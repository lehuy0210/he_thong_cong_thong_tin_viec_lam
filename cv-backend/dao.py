from db import get_db_connection
from mysql.connector import Error

def get_ung_vien_by_id(ma_ung_vien):
    """Lấy thông tin ứng viên. Trả về dict nếu có, None nếu không."""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ung_vien WHERE ma_ung_vien = %s", (ma_ung_vien,))
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
        cursor.execute("SELECT * FROM cv WHERE ma_cv = %s", (ma_cv,))
        return cursor.fetchone()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def create_cv_db(ten_cv, ten_file, hoc_van, kinh_nghiem_lam_viec, ma_ung_vien):
    """Tạo CV mới với đầy đủ các trường theo ERD"""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor(dictionary=True)
        insert_query = """
            INSERT INTO cv (ten_cv, ten_file, hoc_van, kinh_nghiem_lam_viec, ma_ung_vien) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (ten_cv, ten_file, hoc_van, kinh_nghiem_lam_viec, ma_ung_vien))
        conn.commit()
        return cursor.lastrowid
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def update_cv_db(ma_cv, ten_cv=None, ten_file=None, hoc_van=None, kinh_nghiem_lam_viec=None):
    """Cập nhật động thông tin CV (Partial Update)"""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor()
        fields = []
        values = []
        
        mapping = {
            'ten_cv': ten_cv,
            'ten_file': ten_file,
            'hoc_van': hoc_van,
            'kinh_nghiem_lam_viec': kinh_nghiem_lam_viec
        }

        for column, val in mapping.items():
            if val is not None:
                fields.append(f"{column} = %s")
                values.append(val)

        if not fields:
            return False

        values.append(ma_cv)
        update_query = f"UPDATE cv SET {', '.join(fields)} WHERE ma_cv = %s"
        cursor.execute(update_query, tuple(values))
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
        delete_query = "DELETE FROM cv WHERE ma_cv = %s"
        cursor.execute(delete_query, (ma_cv,))
        conn.commit()
        return True
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def create_job_db(tieu_de, mo_ta, ma_trang_thai, han_nop, luong, quyen_loi, ma_nha_tuyen_dung):
    """Tạo tin tuyển dụng mới với đầy đủ các trường theo ERD"""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor(dictionary=True)
        insert_query = """
            INSERT INTO tin_tuyen_dung (tieu_de, mo_ta, ma_trang_thai, han_nop, luong, quyen_loi, ma_nha_tuyen_dung) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (tieu_de, mo_ta, ma_trang_thai, han_nop, luong, quyen_loi, ma_nha_tuyen_dung))
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
        cursor.execute("SELECT * FROM tin_tuyen_dung WHERE tin_id = %s", (tin_id,))
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
        cursor.execute("SELECT * FROM tin_tuyen_dung")
        return cursor.fetchall()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def update_job_db(tin_id, tieu_de=None, mo_ta=None, ma_trang_thai=None, han_nop=None, luong=None, quyen_loi=None):
    """Cập nhật tin tuyển dụng động cho tất cả các trường có trong ERD"""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor()
        fields = []
        values = []
        
        mapping = {
            'tieu_de': tieu_de,
            'mo_ta': mo_ta,
            'ma_trang_thai': ma_trang_thai, 
            'han_nop': han_nop,
            'luong': luong,
            'quyen_loi': quyen_loi
        }

        for column, val in mapping.items():
            if val is not None:
                fields.append(f"{column} = %s")
                values.append(val)

        if not fields:
            return False

        values.append(tin_id)
        update_query = f"UPDATE tin_tuyen_dung SET {', '.join(fields)} WHERE tin_id = %s"
        cursor.execute(update_query, tuple(values))
        conn.commit()
        return True
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def delete_job_db(tin_id):
    """Xóa tin tuyển dụng"""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tin_tuyen_dung WHERE tin_id = %s", (tin_id,))
        conn.commit()
        return cursor.rowcount > 0 
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_nha_tuyen_dung_by_id(ma_nha_tuyen_dung):
    """Lấy thông tin nhà tuyển dụng theo ID"""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM nha_tuyen_dung WHERE ma_nha_tuyen_dung = %s", (ma_nha_tuyen_dung,))
        return cursor.fetchone()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def luu_ho_so_ung_tuyen(ma_ung_vien, tin_id, ma_cv):
    """Lưu hồ sơ ứng tuyển bằng Raw SQL"""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT ma_trang_thai FROM trang_thai WHERE ten_trang_thai = 'Chờ duyệt'")
        trang_thai = cursor.fetchone()
        ma_trang_thai = trang_thai['ma_trang_thai'] if trang_thai else 1
        
        # 2. Insert hồ sơ ứng tuyển mới
        insert_query = """
            INSERT INTO ho_so_ung_tuyen (ma_ung_vien, tin_id, ma_cv, ma_trang_thai, ngay_nop) 
            VALUES (%s, %s, %s, %s, %s)
        """
        ngay_nop = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') 
        
        cursor.execute(insert_query, (ma_ung_vien, tin_id, ma_cv, ma_trang_thai, ngay_nop))
        conn.commit()
        return True
    except Exception as e:
        print(f"Lỗi lưu hồ sơ: {e}")
        return False
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def lay_cv_cua_ung_vien(ma_cv, ma_ung_vien):
    """Lấy thông tin CV để kiểm tra định dạng file bằng Raw SQL"""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM cv WHERE ma_cv = %s AND ma_ung_vien = %s"
        cursor.execute(query, (ma_cv, ma_ung_vien))
        return cursor.fetchone()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()