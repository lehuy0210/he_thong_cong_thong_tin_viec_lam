from flask import Blueprint, request, jsonify
from dao import get_ung_vien_by_id, get_cv_by_id, create_cv_db, update_cv_db, delete_cv_db

cv_bp = Blueprint('cv', __name__)

@cv_bp.route('/cv', methods=['POST'])
def create_cv():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Vui lòng cung cấp dữ liệu JSON!'}), 400

    ten_cv = data.get('TenCV')
    ten_file = data.get('TenFile')
    hoc_van = data.get('HocVan')
    kinh_nghiem_lam_viec = data.get('KinhNghiemLamViec')
    ma_ung_vien = data.get('MaUngVien')

    if not ten_file or not ma_ung_vien:
        return jsonify({'message': 'TenFile và MaUngVien là bắt buộc!'}), 400

    try:
        ung_vien = get_ung_vien_by_id(ma_ung_vien)
        if not ung_vien:
            return jsonify({'message': 'Mã ứng viên không tồn tại!'}), 404

        # Truyền đầy đủ các tham số tương ứng với cơ sở dữ liệu
        ma_cv = create_cv_db(ten_cv, ten_file, hoc_van, kinh_nghiem_lam_viec, ma_ung_vien)

        return jsonify({
            'message': 'Tạo CV thành công!',
            'cv': {
                'MaCV': ma_cv,
                'TenCV': ten_cv,
                'TenFile': ten_file,
                'HocVan': hoc_van,
                'KinhNghiemLamViec': kinh_nghiem_lam_viec,
                'MaUngVien': ma_ung_vien
            }
        }), 201

    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500


@cv_bp.route('/cv/<int:ma_cv>', methods=['PUT'])
def update_cv(ma_cv):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Vui lòng cung cấp dữ liệu JSON!'}), 400

    ten_cv = data.get('TenCV')
    ten_file = data.get('TenFile')
    hoc_van = data.get('HocVan')
    kinh_nghiem_lam_viec = data.get('KinhNghiemLamViec')

    if not ten_file:
        return jsonify({'message': 'TenFile là bắt buộc để cập nhật!'}), 400

    try:
        cv = get_cv_by_id(ma_cv)
        if not cv:
            return jsonify({'message': 'CV không tồn tại!'}), 404

        # Cập nhật đầy đủ các trường dữ liệu theo ERD
        update_cv_db(ma_cv, ten_cv, ten_file, hoc_van, kinh_nghiem_lam_viec)

        return jsonify({
            'message': 'Cập nhật CV thành công!',
            'cv': {
                'MaCV': ma_cv,
                'TenCV': ten_cv,
                'TenFile': ten_file,
                'HocVan': hoc_van,
                'KinhNghiemLamViec': kinh_nghiem_lam_viec,
                'MaUngVien': cv['MaUngVien']
            }
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
            'MaCV': ma_cv
        }), 200

    except Exception as e:
        return jsonify({'message': f'Lỗi hệ thống: {str(e)}'}), 500