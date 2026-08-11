from flask import Blueprint, request, jsonify
from dao import get_ung_vien_by_id, get_cv_by_id, create_cv_db, update_cv_db, delete_cv_db, filter_cvs

cv_bp = Blueprint('cv', __name__)

@cv_bp.route('/cv', methods=['POST'])
def create_cv():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Vui lòng cung cấp dữ liệu JSON!'}), 400

    ten_cv = data.get('ten_cv')
    ten_file = data.get('ten_file')
    hoc_van = data.get('hoc_van')
    kinh_nghiem_lam_viec = data.get('kinh_nghiem_lam_viec')
    ma_ung_vien = data.get('ma_ung_vien')

    # Kiểm tra các trường bắt buộc
    if not ten_file or not ma_ung_vien:
        return jsonify({'message': 'ten_file và ma_ung_vien là bắt buộc!'}), 400

    try:
        # Ràng buộc khóa ngoại: Kiểm tra ứng viên có tồn tại không
        ung_vien = get_ung_vien_by_id(ma_ung_vien)
        if not ung_vien:
            return jsonify({'message': 'Mã ứng viên không tồn tại!'}), 404

        # Lưu vào CSDL
        ma_cv = create_cv_db(ten_cv, ten_file, hoc_van, kinh_nghiem_lam_viec, ma_ung_vien)

        return jsonify({
            'message': 'Tạo CV thành công!',
            'cv': {
                'ma_cv': ma_cv,
                'ten_cv': ten_cv,
                'ten_file': ten_file,
                'hoc_van': hoc_van,
                'kinh_nghiem_lam_viec': kinh_nghiem_lam_viec,
                'ma_ung_vien': ma_ung_vien
            }
        }), 201

    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500


@cv_bp.route('/cv/<int:ma_cv>', methods=['PUT'])
def update_cv(ma_cv):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Vui lòng cung cấp dữ liệu JSON!'}), 400

    ten_cv = data.get('ten_cv')
    ten_file = data.get('ten_file')
    hoc_van = data.get('hoc_van')
    kinh_nghiem_lam_viec = data.get('kinh_nghiem_lam_viec')

    # Yêu cầu ít nhất 1 trường để cập nhật (thay vì bắt buộc ten_file)
    if all(v is None for v in [ten_cv, ten_file, hoc_van, kinh_nghiem_lam_viec]):
        return jsonify({'message': 'Phải truyền ít nhất một trường để cập nhật'}), 400

    try:
        cv = get_cv_by_id(ma_cv)
        if not cv:
            return jsonify({'message': 'CV không tồn tại!'}), 404

        update_cv_db(ma_cv, ten_cv, ten_file, hoc_van, kinh_nghiem_lam_viec)

        # Lấy lại data mới nhất từ DB để trả về cho client
        cv_updated = get_cv_by_id(ma_cv)

        return jsonify({
            'message': 'Cập nhật CV thành công!',
            'cv': cv_updated
        }), 200

    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500


@cv_bp.route('/cv/<int:ma_cv>', methods=['DELETE'])
def delete_cv(ma_cv):
    try:
        cv = get_cv_by_id(ma_cv)
        if not cv:
            return jsonify({'message': 'CV không tồn tại!'}), 404
        delete_cv_db(ma_cv)

        return jsonify({
            'message': 'Xóa CV thành công!',
            'ma_cv': ma_cv
        }), 200

    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500


@cv_bp.route('/cvs/filter', methods=['GET'])
def get_filtered_cvs():
    tin_id = request.args.get('tin_id', type=int)
    hoc_van = request.args.get('hoc_van')
    skills_raw = request.args.get('skills') # "1,2,3"
    
    ds_ma_ky_nang = []
    if skills_raw:
        try:
            ds_ma_ky_nang = [int(x.strip()) for x in skills_raw.split(',') if x.strip()]
        except ValueError:
            return jsonify({'message': 'Danh sách mã kỹ năng không hợp lệ'}), 400

    try:
        cvs = filter_cvs(tin_id=tin_id, ds_ma_ky_nang=ds_ma_ky_nang, tu_khoa_hoc_van=hoc_van)
        return jsonify({'cvs': cvs}), 200
    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500