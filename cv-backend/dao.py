# dao.py
from db import get_db_connection
from mysql.connector import Error

def get_ung_vien_by_id(ma_ung_vien):
    """Lấy thông tin ứng viên. Trả về dict nếu có, None nếu không."""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ungvien WHERE Id = %s", (ma_ung_vien,))
        return cursor.fetchone()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def get_cv_by_id(ma_cv):
    """Lấy thông tin CV theo mã CV"""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cv WHERE MaCV = %s", (ma_cv,))
        return cursor.fetchone()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def create_cv_db(ten_file, ma_ung_vien):
    """Tạo CV mới và trả về ID của CV vừa tạo"""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor(dictionary=True)
        insert_query = "INSERT INTO cv (TenFile, MaUngVien) VALUES (%s, %s)"
        cursor.execute(insert_query, (ten_file, ma_ung_vien))
        conn.commit()
        return cursor.lastrowid
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def update_cv_db(ma_cv, ten_file):
    """Cập nhật tên file cho CV"""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor(dictionary=True)
        update_query = "UPDATE cv SET TenFile = %s WHERE MaCV = %s"
        cursor.execute(update_query, (ten_file, ma_cv))
        conn.commit()
        return True
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def delete_cv_db(ma_cv):
    """Xóa CV"""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor(dictionary=True)
        delete_query = "DELETE FROM cv WHERE MaCV = %s"
        cursor.execute(delete_query, (ma_cv,))
        conn.commit()
        return True
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def create_job_db(tieu_de, mo_ta, ma_nha_tuyen_dung):
    """Tạo tin tuyển dụng mới, trả về ID của tin vừa tạo"""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor(dictionary=True)
        insert_query = "INSERT INTO tintuyendung (TieuDe, MoTa, MaNhaTuyenDung) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (tieu_de, mo_ta, ma_nha_tuyen_dung))
        conn.commit()
        return cursor.lastrowid
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def get_job_by_id(tin_id):
    """Lấy thông tin một tin tuyển dụng theo ID"""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT TinId, TieuDe, MoTa, MaNhaTuyenDung FROM tintuyendung WHERE TinId = %s", (tin_id,))
        return cursor.fetchone()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def get_all_jobs_db():
    """Lấy danh sách tất cả tin tuyển dụng"""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT TinId, TieuDe, MoTa, MaNhaTuyenDung FROM tintuyendung")
        return cursor.fetchall()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def update_job_db(tin_id, tieu_de=None, mo_ta=None):
    """Cập nhật tin tuyển dụng động (truyền gì update nấy)"""
    if tieu_de is None and mo_ta is None:
        return False
        
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor()
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
        return True
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def delete_job_db(tin_id):
    """Xóa tin tuyển dụng, trả về True nếu xóa thành công, False nếu không tìm thấy"""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tintuyendung WHERE TinId = %s", (tin_id,))
        conn.commit()
        return cursor.rowcount > 0 
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()