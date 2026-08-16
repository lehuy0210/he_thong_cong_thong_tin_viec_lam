from flask import request, redirect, url_for, flash
import dao
HOP_LE = ['.pdf', '.doc', '.docx']

@app.route('/cong-viec/<int:tin_id>/ung-tuyen', methods=['POST'])
def ung_tuyen_cong_viec(tin_id):
    ma_ung_vien = current_user.id 
    
    ma_cv_duoc_chon = request.form.get('ma_cv')
    
    if not ma_cv_duoc_chon:
        flash("Vui lòng chọn CV để ứng tuyển.", "warning")
        return redirect(url_for('chi_tiet_cong_viec', tin_id=tin_id))

    cv = dao.lay_cv_cua_ung_vien(ma_cv=ma_cv_duoc_chon, ma_ung_vien=ma_ung_vien)
    
    if cv:
        duoi_file = '.' + cv.ten_file.rsplit('.', 1)[1].lower() if '.' in cv.ten_file else ''
        
        if duoi_file not in HOP_LE:
            flash("Định dạng file CV bị sai. Vui lòng dùng file .pdf, .doc hoặc .docx", "error")
            return redirect(url_for('chi_tiet_cong_viec', tin_id=tin_id))
    else:
        flash("CV không tồn tại.", "error")
        return redirect(url_for('chi_tiet_cong_viec', tin_id=tin_id))

    thanh_cong = dao.luu_ho_so_ung_tuyen(ma_ung_vien, tin_id, cv.ma_cv)
    
    if thanh_cong:
        flash("Nộp hồ sơ thành công! Hồ sơ của bạn đã được lưu vào hệ thống.", "success")
    else:
        flash("Có lỗi xảy ra, không thể nộp hồ sơ lúc này.", "error")
        
    return redirect(url_for('chi_tiet_cong_viec', tin_id=tin_id))