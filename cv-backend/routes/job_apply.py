from flask import Blueprint, request, jsonify
import dao

job_apply_bp = Blueprint('job_apply', __name__)

HOP_LE = ['.pdf', '.doc', '.docx']

@job_apply_bp.route('/cong-viec/<int:tin_id>/ung-tuyen', methods=['POST'])
def ung_tuyen_cong_viec(tin_id):
    try:
        data = request.json
        if not data:
            return jsonify({"ok": False, "message": "Không nhận được dữ liệu."}), 400

        ma_ung_vien = data.get('ma_ung_vien') 
        ma_cv_duoc_chon = data.get('ma_cv')
        
        if not ma_cv_duoc_chon:
            return jsonify({"ok": False, "message": "Vui lòng chọn CV để ứng tuyển."}), 400
            
        if not ma_ung_vien:
            return jsonify({"ok": False, "message": "Lỗi xác thực: Không tìm thấy thông tin ứng viên."}), 401

        cv = dao.lay_cv_cua_ung_vien(ma_cv=ma_cv_duoc_chon, ma_ung_vien=ma_ung_vien)
        
        if cv:
            duoi_file = '.' + cv.ten_file.rsplit('.', 1)[1].lower() if '.' in cv.ten_file else ''
            
            if duoi_file not in HOP_LE:
                return jsonify({"ok": False, "message": "Định dạng file CV bị sai. Vui lòng dùng file .pdf, .doc hoặc .docx"}), 400
        else:
            return jsonify({"ok": False, "message": "CV không tồn tại hoặc không thuộc quyền sở hữu của bạn."}), 404

        thanh_cong = dao.luu_ho_so_ung_tuyen(ma_ung_vien, tin_id, cv.ma_cv)
        
        if thanh_cong:
            return jsonify({"ok": True, "message": "Nộp hồ sơ thành công! Hồ sơ của bạn đã được lưu vào hệ thống."}), 200
        else:
            return jsonify({"ok": False, "message": "Có lỗi xảy ra, không thể nộp hồ sơ lúc này."}), 500

    except Exception as e:
        return jsonify({"ok": False, "message": f"Lỗi hệ thống: {str(e)}"}), 500