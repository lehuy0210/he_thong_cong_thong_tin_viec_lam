from flask import Blueprint, request, jsonify
from dao import create_job_db, get_job_by_id, get_all_jobs_db, update_job_db, delete_job_db, get_nha_tuyen_dung_by_id, filter_jobs

job_bp = Blueprint('job', __name__)

@job_bp.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Vui lòng gửi dữ liệu JSON'}), 400
        
    tieu_de = data.get('tieu_de')
    mo_ta = data.get('mo_ta')
    han_nop = data.get('han_nop')
    luong = data.get('luong')
    quyen_loi = data.get('quyen_loi')
    ma_nha_tuyen_dung = data.get('ma_nha_tuyen_dung')
    ma_trang_thai = data.get('ma_trang_thai') 

    if not tieu_de or not ma_nha_tuyen_dung:
        return jsonify({'message': 'tieu_de và ma_nha_tuyen_dung là bắt buộc'}), 400

    try:
        nha_tuyen_dung = get_nha_tuyen_dung_by_id(ma_nha_tuyen_dung)
        if not nha_tuyen_dung:
            return jsonify({'message': 'Mã nhà tuyển dụng không tồn tại!'}), 404

        tin_id = create_job_db(tieu_de, mo_ta, ma_trang_thai, han_nop, luong, quyen_loi, ma_nha_tuyen_dung)

        return jsonify({
            'message': 'Tạo tin tuyển dụng thành công',
            'tin': {
                'tin_id': tin_id,
                'tieu_de': tieu_de,
                'mo_ta': mo_ta,
                'ma_trang_thai': ma_trang_thai,
                'han_nop': han_nop,
                'luong': luong,
                'quyen_loi': quyen_loi,
                'ma_nha_tuyen_dung': ma_nha_tuyen_dung
            }
        }), 201

    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500


@job_bp.route('/jobs/<int:tin_id>', methods=['PUT'])
def update_job(tin_id):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Vui lòng gửi dữ liệu JSON'}), 400

    tieu_de = data.get('tieu_de')
    mo_ta = data.get('mo_ta')
    han_nop = data.get('han_nop')
    luong = data.get('luong')
    quyen_loi = data.get('quyen_loi')
    ma_trang_thai = data.get('ma_trang_thai')

    if all(v is None for v in [tieu_de, mo_ta, ma_trang_thai, han_nop, luong, quyen_loi]):
        return jsonify({'message': 'Phải truyền ít nhất một trường để cập nhật'}), 400

    try:
        tin = get_job_by_id(tin_id)
        if not tin:
            return jsonify({'message': 'Không tìm thấy tin tuyển dụng'}), 404

        update_job_db(tin_id, tieu_de, mo_ta, ma_trang_thai, han_nop, luong, quyen_loi)
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
        keyword = request.args.get('keyword')
        luong_min = request.args.get('luong_min')
        luong_max = request.args.get('luong_max')
        
        if luong_min is not None:
            try:
                luong_min = int(luong_min)
            except ValueError:
                luong_min = None
                
        if luong_max is not None:
            try:
                luong_max = int(luong_max)
            except ValueError:
                luong_max = None
                
        if keyword or luong_min is not None or luong_max is not None:
            jobs = filter_jobs(keyword=keyword, luong_min=luong_min, luong_max=luong_max)
        else:
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