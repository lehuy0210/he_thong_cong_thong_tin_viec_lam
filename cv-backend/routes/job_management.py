from flask import Blueprint, request, jsonify
from dao import create_job_db, get_job_by_id, get_all_jobs_db, update_job_db, delete_job_db

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

    try:
        tin_id = create_job_db(tieu_de, mo_ta, ma_nha_tuyen_dung)

        return jsonify({
            'message': 'Tạo tin tuyển dụng thành công',
            'tin': {
                'TinId': tin_id,
                'TieuDe': tieu_de,
                'MoTa': mo_ta,
                'MaNhaTuyenDung': ma_nha_tuyen_dung
            }
        }), 201

    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500


@job_bp.route('/jobs/<int:tin_id>', methods=['PUT'])
def update_job(tin_id):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Vui lòng gửi dữ liệu JSON'}), 400

    tieu_de = data.get('TieuDe')
    mo_ta = data.get('MoTa')

    if tieu_de is None and mo_ta is None:
        return jsonify({'message': 'Phải truyền ít nhất một trường để cập nhật (TieuDe hoặc MoTa)'}), 400

    try:
        tin = get_job_by_id(tin_id)
        if not tin:
            return jsonify({'message': 'Không tìm thấy tin tuyển dụng'}), 404

        update_job_db(tin_id, tieu_de, mo_ta)
        return jsonify({'message': 'Cập nhật tin tuyển dụng thành công'}), 200

    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500


@job_bp.route('/jobs/<int:tin_id>', methods=['DELETE'])
def delete_job(tin_id):
    try:
        is_deleted = delete_job_db(tin_id)
        
        if not is_deleted:
            return jsonify({'message': 'Không tìm thấy tin tuyển dụng'}), 404

        return jsonify({'message': 'Xóa tin tuyển dụng thành công'}), 200

    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500


@job_bp.route('/jobs', methods=['GET'])
def get_jobs():
    try:
        jobs = get_all_jobs_db()
        return jsonify({'jobs': jobs}), 200
    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500


@job_bp.route('/jobs/<int:tin_id>', methods=['GET'])
def get_job(tin_id):
    try:
        job = get_job_by_id(tin_id)
        if not job:
            return jsonify({'message': 'Không tìm thấy tin tuyển dụng'}), 404
            
        return jsonify({'job': job}), 200
    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500