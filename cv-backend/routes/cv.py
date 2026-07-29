from flask import Blueprint, request, jsonify
from db import get_db_connection
from mysql.connector import Error

cv_bp = Blueprint('cv', __name__)

@cv_bp.route('/cv', methods=['POST'])
def create_cv():
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'Vui lòng cung cấp dữ liệu JSON!'}), 400

    ten_file = data.get('TenFile')
    ma_ung_vien = data.get('MaUngVien')

    if not ten_file or not ma_ung_vien:
        return jsonify({'message': 'TenFile và MaUngVien là bắt buộc!'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Lỗi kết nối cơ sở dữ liệu!'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM ungvien WHERE Id = %s", (ma_ung_vien,))
        ung_vien = cursor.fetchone()
        if not ung_vien:
            return jsonify({'message': 'Mã ứng viên không tồn tại!'}), 404

        insert_query = "INSERT INTO cv (TenFile, MaUngVien) VALUES (%s, %s)"
        cursor.execute(insert_query, (ten_file, ma_ung_vien))
        conn.commit()

        return jsonify({
            'message': 'Tạo CV thành công!',
            'cv': {
                'MaCV': cursor.lastrowid,
                'TenFile': ten_file,
                'MaUngVien': ma_ung_vien
            }
        }), 201

    except Error as e:
        return jsonify({'message': f'Lỗi cơ sở dữ liệu: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@cv_bp.route('/cv/<int:ma_cv>', methods=['PUT'])
def update_cv(ma_cv):
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'Vui lòng cung cấp dữ liệu JSON!'}), 400

    ten_file = data.get('TenFile')

    if not ten_file:
        return jsonify({'message': 'TenFile là bắt buộc để cập nhật!'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Lỗi kết nối cơ sở dữ liệu!'}), 500

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM cv WHERE MaCV = %s", (ma_cv,))
        cv = cursor.fetchone()
        if not cv:
            return jsonify({'message': 'CV không tồn tại!'}), 404

        update_query = "UPDATE cv SET TenFile = %s WHERE MaCV = %s"
        cursor.execute(update_query, (ten_file, ma_cv))
        conn.commit()

        return jsonify({
            'message': 'Cập nhật CV thành công!',
            'cv': {
                'MaCV': ma_cv,
                'TenFile': ten_file,
                'MaUngVien': cv['MaUngVien']
            }
        }), 200

    except Error as e:
        return jsonify({'message': f'Lỗi cơ sở dữ liệu: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@cv_bp.route('/cv/<int:ma_cv>', methods=['DELETE'])
def delete_cv(ma_cv):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Lỗi kết nối cơ sở dữ liệu!'}), 500

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM cv WHERE MaCV = %s", (ma_cv,))
        cv = cursor.fetchone()
        if not cv:
            return jsonify({'message': 'CV không tồn tại!'}), 404

        delete_query = "DELETE FROM cv WHERE MaCV = %s"
        cursor.execute(delete_query, (ma_cv,))
        conn.commit()

        return jsonify({
            'message': 'Xóa CV thành công!',
            'MaCV': ma_cv
        }), 200

    except Error as e:
        return jsonify({'message': f'Lỗi cơ sở dữ liệu: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
