import os
import sqlite3
from datetime import date, datetime
from functools import wraps
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'revenue_commission_secret_key_1995_#_secure')
PIN_CODE = os.environ.get('APP_PIN', '1995')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'revenue.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    conn = get_db()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_info TEXT NOT NULL,
                order_date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                item_name TEXT NOT NULL,
                price REAL NOT NULL DEFAULT 0,
                quantity INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
            );
        """)
        # Indexing for fast period query
        conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_items_order_id ON order_items(order_id);")
    conn.close()


init_db()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            if request.path.startswith('/api/'):
                return jsonify({'success': False, 'message': 'Chưa đăng nhập'}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ------------------ LOGIC CHU KỲ CHỐT SỔ (TỪ NGÀY 9 ĐẾN NGÀY 8) ------------------
def get_cycle_dates(closing_year: int, closing_month: int):
    """
    Kỳ chốt tháng M/Năm Y:
    Kết thúc: 23:59 ngày 08/M/Y
    Bắt đầu: 00:00 ngày 09 của tháng liền trước (M-1)
    """
    end_date = date(closing_year, closing_month, 8)
    start_date = (end_date - relativedelta(months=1)).replace(day=9)
    return start_date, end_date


def get_current_cycle():
    """
    Tự động xác định chu kỳ hiện tại theo ngày hôm nay.
    Nếu ngày hôm nay > 8: Đang thuộc kỳ chốt ngày 08 tháng sau.
    Nếu ngày hôm nay <= 8: Đang thuộc kỳ chốt ngày 08 tháng này.
    """
    today = date.today()
    if today.day > 8:
        closing_dt = today + relativedelta(months=1)
    else:
        closing_dt = today
    return closing_dt.year, closing_dt.month


def get_cycle_metadata(closing_year: int, closing_month: int):
    start_date, end_date = get_cycle_dates(closing_year, closing_month)
    closing_dt = date(closing_year, closing_month, 8)
    prev_dt = closing_dt - relativedelta(months=1)
    next_dt = closing_dt + relativedelta(months=1)

    return {
        'closing_year': closing_year,
        'closing_month': closing_month,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'start_display': start_date.strftime('%d/%m/%Y'),
        'end_display': end_date.strftime('%d/%m/%Y'),
        'cycle_label': f"Kỳ chốt 08/{closing_month:02d}/{closing_year}",
        'cycle_detail': f"Từ 09/{start_date.month:02d}/{start_date.year} đến 08/{closing_month:02d}/{closing_year}",
        'prev_cycle': {'year': prev_dt.year, 'month': prev_dt.month},
        'next_cycle': {'year': next_dt.year, 'month': next_dt.month}
    }


# ------------------ ROUTES ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        pin = request.form.get('pin', '').strip()
        if pin == PIN_CODE:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Mã PIN không chính xác, vui lòng thử lại!")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    cur_year, cur_month = get_current_cycle()
    year = request.args.get('year', default=cur_year, type=int)
    month = request.args.get('month', default=cur_month, type=int)
    
    # Boundary check for valid month
    if month < 1 or month > 12:
        year, month = cur_year, cur_month

    cycle_info = get_cycle_metadata(year, month)
    today_str = date.today().strftime('%Y-%m-%d')
    return render_template('index.html', cycle=cycle_info, today=today_str)


# ------------------ API ENDPOINTS ------------------
@app.route('/api/cycle-orders', methods=['GET'])
@login_required
def api_get_cycle_orders():
    cur_year, cur_month = get_current_cycle()
    year = request.args.get('year', default=cur_year, type=int)
    month = request.args.get('month', default=cur_month, type=int)

    cycle_info = get_cycle_metadata(year, month)
    start_date = cycle_info['start_date']
    end_date = cycle_info['end_date']

    conn = get_db()
    
    # Query orders within cycle dates
    orders_rows = conn.execute("""
        SELECT id, customer_info, order_date, created_at
        FROM orders
        WHERE order_date >= ? AND order_date <= ?
        ORDER BY order_date DESC, id DESC;
    """, (start_date, end_date)).fetchall()

    orders_list = []
    total_cycle_revenue = 0.0

    for order_row in orders_rows:
        order_id = order_row['id']
        items_rows = conn.execute("""
            SELECT id, item_name, price, quantity
            FROM order_items
            WHERE order_id = ?
            ORDER BY id ASC;
        """, (order_id,)).fetchall()

        items = []
        order_total = 0.0
        for item in items_rows:
            p = float(item['price'])
            q = int(item['quantity'])
            subtotal = p * q
            item_comm = round(subtotal * 0.04, 2)
            order_total += subtotal
            items.append({
                'id': item['id'],
                'item_name': item['item_name'],
                'price': p,
                'quantity': q,
                'subtotal': subtotal,
                'commission': item_comm
            })

        order_commission = round(order_total * 0.04, 2)
        total_cycle_revenue += order_total

        # Format display date (dd/mm/yyyy)
        try:
            d_obj = datetime.strptime(order_row['order_date'], '%Y-%m-%d')
            date_display = d_obj.strftime('%d/%m/%Y')
        except Exception:
            date_display = order_row['order_date']

        orders_list.append({
            'id': order_id,
            'customer_info': order_row['customer_info'],
            'order_date': order_row['order_date'],
            'date_display': date_display,
            'created_at': order_row['created_at'],
            'items': items,
            'items_count': len(items),
            'total_amount': order_total,
            'commission_4pct': order_commission
        })

    conn.close()

    total_cycle_commission = round(total_cycle_revenue * 0.04, 2)

    return jsonify({
        'success': True,
        'cycle': cycle_info,
        'summary': {
            'total_orders': len(orders_list),
            'total_revenue': total_cycle_revenue,
            'total_commission': total_cycle_commission,
            'commission_rate': 0.04
        },
        'orders': orders_list
    })


@app.route('/api/orders/<int:order_id>', methods=['GET'])
@login_required
def api_get_order(order_id):
    conn = get_db()
    order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if not order:
        conn.close()
        return jsonify({'success': False, 'message': 'Không tìm thấy hóa đơn'}), 404

    items = conn.execute("SELECT * FROM order_items WHERE order_id = ? ORDER BY id ASC", (order_id,)).fetchall()
    conn.close()

    return jsonify({
        'success': True,
        'order': {
            'id': order['id'],
            'customer_info': order['customer_info'],
            'order_date': order['order_date'],
            'items': [{
                'id': it['id'],
                'item_name': it['item_name'],
                'price': float(it['price']),
                'quantity': int(it['quantity'])
            } for it in items]
        }
    })


@app.route('/api/orders', methods=['POST'])
@login_required
def api_create_order():
    data = request.get_json() or {}
    customer_info = (data.get('customer_info') or '').strip()
    order_date = (data.get('order_date') or '').strip()
    items = data.get('items', [])

    if not customer_info:
        return jsonify({'success': False, 'message': 'Vui lòng nhập Biển số xe hoặc Tên khách'}), 400
    if not order_date:
        return jsonify({'success': False, 'message': 'Vui lòng chọn ngày tạo đơn'}), 400
    if not items or not isinstance(items, list) or len(items) == 0:
        return jsonify({'success': False, 'message': 'Hóa đơn phải có ít nhất 1 món hàng'}), 400

    # Validate items
    valid_items = []
    for idx, item in enumerate(items):
        item_name = (item.get('item_name') or '').strip()
        if not item_name:
            return jsonify({'success': False, 'message': f'Dòng {idx+1}: Tên món không được để trống'}), 400
        try:
            price = float(item.get('price', 0))
            if price < 0:
                raise ValueError()
        except (ValueError, TypeError):
            return jsonify({'success': False, 'message': f'Dòng {idx+1}: Đơn giá không hợp lệ'}), 400

        try:
            quantity = int(item.get('quantity', 1))
            if quantity < 1:
                quantity = 1
        except (ValueError, TypeError):
            quantity = 1

        valid_items.append((item_name, price, quantity))

    conn = get_db()
    with conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (customer_info, order_date)
            VALUES (?, ?)
        """, (customer_info, order_date))
        order_id = cursor.lastrowid

        for item_name, price, quantity in valid_items:
            cursor.execute("""
                INSERT INTO order_items (order_id, item_name, price, quantity)
                VALUES (?, ?, ?, ?)
            """, (order_id, item_name, price, quantity))

    conn.close()
    return jsonify({'success': True, 'message': 'Tạo đơn hàng thành công!', 'order_id': order_id})


@app.route('/api/orders/<int:order_id>', methods=['PUT'])
@login_required
def api_update_order(order_id):
    data = request.get_json() or {}
    customer_info = (data.get('customer_info') or '').strip()
    order_date = (data.get('order_date') or '').strip()
    items = data.get('items', [])

    if not customer_info:
        return jsonify({'success': False, 'message': 'Vui lòng nhập Biển số xe hoặc Tên khách'}), 400
    if not order_date:
        return jsonify({'success': False, 'message': 'Vui lòng chọn ngày hóa đơn'}), 400
    if not items or not isinstance(items, list) or len(items) == 0:
        return jsonify({'success': False, 'message': 'Hóa đơn phải có ít nhất 1 món hàng'}), 400

    valid_items = []
    for idx, item in enumerate(items):
        item_name = (item.get('item_name') or '').strip()
        if not item_name:
            return jsonify({'success': False, 'message': f'Dòng {idx+1}: Tên món không được để trống'}), 400
        try:
            price = float(item.get('price', 0))
            if price < 0:
                raise ValueError()
        except (ValueError, TypeError):
            return jsonify({'success': False, 'message': f'Dòng {idx+1}: Đơn giá không hợp lệ'}), 400

        try:
            quantity = int(item.get('quantity', 1))
            if quantity < 1:
                quantity = 1
        except (ValueError, TypeError):
            quantity = 1

        valid_items.append((item_name, price, quantity))

    conn = get_db()
    with conn:
        cursor = conn.cursor()
        # Check order existence
        exist = cursor.execute("SELECT id FROM orders WHERE id = ?", (order_id,)).fetchone()
        if not exist:
            conn.close()
            return jsonify({'success': False, 'message': 'Không tìm thấy hóa đơn'}), 404

        # Update order header
        cursor.execute("""
            UPDATE orders
            SET customer_info = ?, order_date = ?
            WHERE id = ?
        """, (customer_info, order_date, order_id))

        # Clear existing items and re-insert
        cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
        for item_name, price, quantity in valid_items:
            cursor.execute("""
                INSERT INTO order_items (order_id, item_name, price, quantity)
                VALUES (?, ?, ?, ?)
            """, (order_id, item_name, price, quantity))

    conn.close()
    return jsonify({'success': True, 'message': 'Cập nhật đơn hàng thành công!'})


@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
@login_required
def api_delete_order(order_id):
    conn = get_db()
    with conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'success': False, 'message': 'Không tìm thấy đơn hàng cần xóa'}), 404
    conn.close()
    return jsonify({'success': True, 'message': 'Đã xóa đơn hàng thành công!'})


if __name__ == '__main__':
    # Local development server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
