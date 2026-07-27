from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from db import get_db_connection  # Import hàm kết nối

# Tạo blueprint cho các API liên quan đến xác thực (auth)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'Vui lòng cung cấp dữ liệu JSON!'}), 400

    username = data.get('Username')
    password = data.get('Password')
    vai_tro = data.get('VaiTro') 

    if not username or not password or not vai_tro:
        return jsonify({'message': 'Username, Password và VaiTro là bắt buộc!'}), 400

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Lỗi kết nối cơ sở dữ liệu!'}), 500

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM nguoidung WHERE Username = %s", (username,))
        if cursor.fetchone():
            return jsonify({'message': 'Tên đăng nhập (Username) đã tồn tại!'}), 409

        insert_query = "INSERT INTO nguoidung (Username, Password, VaiTro) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (username, hashed_password, vai_tro))
        conn.commit()

        return jsonify({
            'message': 'Đăng ký tài khoản thành công!',
            'user': {
                'Id': cursor.lastrowid,
                'Username': username,
                'VaiTro': vai_tro
            }
        }), 201

    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()