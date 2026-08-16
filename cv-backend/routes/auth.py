from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash 
from db import get_db_connection 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'Vui lòng cung cấp dữ liệu JSON!'}), 400

    username = data.get('Username')
    password = data.get('Password')

    if not username or not password:
        return jsonify({'message': 'Username và Password là bắt buộc!'}), 400

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Lỗi kết nối cơ sở dữ liệu!'}), 500

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM nguoi_dung WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({'message': 'Tên đăng nhập (Username) đã tồn tại!'}), 409

        ma_vai_tro_mac_dinh = 1 

        insert_query = "INSERT INTO nguoi_dung (username, password, ma_vai_tro) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (username, hashed_password, ma_vai_tro_mac_dinh))
        conn.commit()

        return jsonify({
            'message': 'Đăng ký tài khoản thành công!',
            'user': {
                'Id': cursor.lastrowid,
                'Username': username,
                'ma_vai_tro': ma_vai_tro_mac_dinh
            }
        }), 201

    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'Vui lòng cung cấp dữ liệu JSON!'}), 400

    username = data.get('Username')
    password = data.get('Password')

    if not username or not password:
        return jsonify({'message': 'Username và Password là bắt buộc!'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Lỗi kết nối cơ sở dữ liệu!'}), 500

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM nguoi_dung WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            return jsonify({
                'message': 'Đăng nhập thành công!',
                'user': {
                    'Id': user['id'],
                    'Username': user['username'],
                    'ma_vai_tro': user['ma_vai_tro']
                }
            }), 200
        else:
            return jsonify({'message': 'Sai tài khoản hoặc mật khẩu!'}), 401

    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn and conn.is_connected():
            conn.close()