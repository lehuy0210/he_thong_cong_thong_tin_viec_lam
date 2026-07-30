from flask import Blueprint, request, jsonify
from db import get_db_connection

# Blueprint cho quản lý tin tuyển dụng
job_bp = Blueprint('job', __name__)


@job_bp.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Vui lòng gửi dữ liệu JSON'}), 400

    tieu_de = data.get('TieuDe')
    mo_ta = data.get('MoTa')
    ma_nha_tuyen_dung = data.get('MaNhaTuyenDung')

    if not tieu_de or not ma_nha_tuyen_dung:
        return jsonify({'message': 'TieuDe và MaNhaTuyenDung là bắt buộc'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Lỗi kết nối cơ sở dữ liệu!'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        insert_query = "INSERT INTO tintuyendung (TieuDe, MoTa, MaNhaTuyenDung) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (tieu_de, mo_ta, ma_nha_tuyen_dung))
        conn.commit()

        return jsonify({
            'message': 'Tạo tin tuyển dụng thành công',
            'tin': {
                'TinId': cursor.lastrowid,
                'TieuDe': tieu_de,
                'MoTa': mo_ta,
                'MaNhaTuyenDung': ma_nha_tuyen_dung
            }
        }), 201

    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@job_bp.route('/jobs/<int:tin_id>', methods=['PUT'])
def update_job(tin_id):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Vui lòng gửi dữ liệu JSON'}), 400

    tieu_de = data.get('TieuDe')
    mo_ta = data.get('MoTa')

    if not tieu_de and not mo_ta:
        return jsonify({'message': 'Phải truyền ít nhất một trường để cập nhật (TieuDe hoặc MoTa)'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Lỗi kết nối cơ sở dữ liệu!'}), 500

    try:
        cursor = conn.cursor()

        # Kiểm tra tin tồn tại
        cursor.execute("SELECT * FROM tintuyendung WHERE TinId = %s", (tin_id,))
        if cursor.fetchone() is None:
            return jsonify({'message': 'Không tìm thấy tin tuyển dụng'}), 404

        # Xây dựng câu lệnh UPDATE động
        fields = []
        values = []
        if tieu_de is not None:
            fields.append('TieuDe = %s')
            values.append(tieu_de)
        if mo_ta is not None:
            fields.append('MoTa = %s')
            values.append(mo_ta)

        values.append(tin_id)
        update_query = f"UPDATE tintuyendung SET {', '.join(fields)} WHERE TinId = %s"
        cursor.execute(update_query, tuple(values))
        conn.commit()

        return jsonify({'message': 'Cập nhật tin tuyển dụng thành công'}), 200

    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@job_bp.route('/jobs/<int:tin_id>', methods=['DELETE'])
def delete_job(tin_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Lỗi kết nối cơ sở dữ liệu!'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tintuyendung WHERE TinId = %s", (tin_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'message': 'Không tìm thấy tin tuyển dụng'}), 404

        return jsonify({'message': 'Xóa tin tuyển dụng thành công'}), 200

    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@job_bp.route('/jobs', methods=['GET'])
def get_jobs():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Lỗi kết nối cơ sở dữ liệu!'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT TinId, TieuDe, MoTa, MaNhaTuyenDung FROM tintuyendung")
        rows = cursor.fetchall()
        return jsonify({'jobs': rows}), 200

    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@job_bp.route('/jobs/<int:tin_id>', methods=['GET'])
def get_job(tin_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Lỗi kết nối cơ sở dữ liệu!'}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT TinId, TieuDe, MoTa, MaNhaTuyenDung FROM tintuyendung WHERE TinId = %s", (tin_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({'message': 'Không tìm thấy tin tuyển dụng'}), 404
        return jsonify({'job': row}), 200

    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
