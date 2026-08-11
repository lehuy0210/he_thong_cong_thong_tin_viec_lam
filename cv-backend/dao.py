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
            
def filter_jobs(
    keyword=None,
    luong_min=None,
    luong_max=None,
):
    """Tìm kiếm và lọc tin tuyển dụng theo từ khóa và mức lương (chỉ lấy các tin có trạng thái 'Đang mở')."""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT t.* 
            FROM tin_tuyen_dung t
            JOIN trang_thai ts ON t.ma_trang_thai = ts.ma_trang_thai
            WHERE ts.ten_trang_thai = %s
        """
        params = ["Đang mở"]

        if keyword:
            query += " AND (t.tieu_de LIKE %s OR t.mo_ta LIKE %s)"
            params.append(f"%{keyword}%")
            params.append(f"%{keyword}%")

        if luong_min is not None:
            query += " AND t.luong >= %s"
            params.append(luong_min)

        if luong_max is not None:
            query += " AND t.luong <= %s"
            params.append(luong_max)

        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def filter_cvs(tin_id=None, ds_ma_ky_nang=None, tu_khoa_hoc_van=None):
    """Lọc danh sách CV dựa trên tin_id, danh sách mã kỹ năng, và học vấn."""
    conn = get_db_connection()
    if conn is None:
        raise Exception("Lỗi kết nối cơ sở dữ liệu!")
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Xây dựng câu truy vấn động
        query = """
            SELECT 
                c.ma_cv, 
                c.ten_cv, 
                c.ten_file, 
                c.hoc_van, 
                c.kinh_nghiem_lam_viec, 
                c.ma_ung_vien,
                uv.ho_ten,
                uv.email,
                COUNT(ckn.ma_ky_nang) AS so_ky_nang_trung_khop
            FROM cv c
            JOIN ung_vien uv ON c.ma_ung_vien = uv.ma_ung_vien
        """
        
        params = []
        joins = ""
        where_conds = []
        
        # 1. Nếu lọc theo tin_id (lọc từ các hồ sơ ứng tuyển của tin đó)
        if tin_id is not None:
            joins += " JOIN ho_so_ung_tuyen h ON c.ma_cv = h.ma_cv "
            where_conds.append("h.tin_id = %s")
            params.append(tin_id)
            
        # 2. Nếu có lọc theo danh sách kỹ năng
        if ds_ma_ky_nang:
            joins += " LEFT JOIN cv_ky_nang ckn ON c.ma_cv = ckn.ma_cv "
            placeholders = ", ".join(["%s"] * len(ds_ma_ky_nang))
            where_conds.append(f"ckn.ma_ky_nang IN ({placeholders})")
            params.extend(ds_ma_ky_nang)
        else:
            # Nếu không lọc kỹ năng, vẫn JOIN để đếm kỹ năng trùng khớp (trả về 0)
            joins += " LEFT JOIN cv_ky_nang ckn ON c.ma_cv = ckn.ma_cv "
            
        # 3. Lọc theo từ khóa học vấn
        if tu_khoa_hoc_van:
            where_conds.append("c.hoc_van LIKE %s")
            params.append(f"%{tu_khoa_hoc_van}%")
            
        query += joins
        if where_conds:
            query += " WHERE " + " AND ".join(where_conds)
            
        query += " GROUP BY c.ma_cv "
        
        # Sắp xếp theo số lượng kỹ năng khớp từ cao xuống thấp
        query += " ORDER BY so_ky_nang_trung_khop DESC"
        
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()