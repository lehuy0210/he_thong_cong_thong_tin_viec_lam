from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ========================================================
# BẢNG TRUNG GIAN (N - N)
# ========================================================
cv_ky_nang = db.Table('cv_ky_nang',
    db.Column('ma_cv', db.Integer, db.ForeignKey('cv.ma_cv', ondelete='CASCADE'), primary_key=True),
    db.Column('ma_ky_nang', db.Integer, db.ForeignKey('ky_nang.ma_ky_nang', ondelete='CASCADE'), primary_key=True)
)

tin_tuyen_dung_ky_nang = db.Table('tin_tuyen_dung_ky_nang',
    db.Column('tin_id', db.Integer, db.ForeignKey('tin_tuyen_dung.tin_id', ondelete='CASCADE'), primary_key=True),
    db.Column('ma_ky_nang', db.Integer, db.ForeignKey('ky_nang.ma_ky_nang', ondelete='CASCADE'), primary_key=True)
)

# ========================================================
# 1. CÁC BẢNG DANH MỤC (LOOKUP TABLES)
# ========================================================
class VaiTro(db.Model):
    __tablename__ = 'vai_tro'
    ma_vai_tro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_vai_tro = db.Column(db.String(50), nullable=False, unique=True)
    
    # Quan hệ 1-Nhiều với NguoiDung
    nguoi_dungs = db.relationship('NguoiDung', backref='vai_tro_ref', lazy=True)

class TrangThai(db.Model):
    __tablename__ = 'trang_thai'
    ma_trang_thai = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_trang_thai = db.Column(db.String(50), nullable=False, unique=True)
    
    # Quan hệ 1-Nhiều với TinTuyenDung và HoSoUngTuyen
    tin_tuyen_dungs = db.relationship('TinTuyenDung', backref='trang_thai_ref', lazy=True)
    ho_so_ung_tuyens = db.relationship('HoSoUngTuyen', backref='trang_thai_ref', lazy=True)

class KyNang(db.Model):
    __tablename__ = 'ky_nang'
    ma_ky_nang = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_ky_nang = db.Column(db.String(100), nullable=False, unique=True)

# ========================================================
# 2. BẢNG NGƯỜI DÙNG & CÁC BẢNG KẾ THỪA
# ========================================================
class NguoiDung(db.Model):
    __tablename__ = 'nguoi_dung'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    ma_vai_tro = db.Column(db.Integer, db.ForeignKey('vai_tro.ma_vai_tro', ondelete='RESTRICT'), nullable=False)

class UngVien(db.Model):
    __tablename__ = 'ung_vien'
    ma_ung_vien = db.Column(db.Integer, db.ForeignKey('nguoi_dung.id', ondelete='CASCADE'), primary_key=True)
    ho_ten = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    gioi_tinh = db.Column(db.Enum('Nam', 'Nữ'), nullable=True)
    so_dien_thoai = db.Column(db.String(20), nullable=True)
    ngay_sinh = db.Column(db.Date, nullable=True)
    dia_chi = db.Column(db.Text, nullable=True)
    
    # Quan hệ 1-Nhiều
    cvs = db.relationship('CV', backref='ung_vien_ref', cascade='all, delete-orphan')
    ho_so_ung_tuyens = db.relationship('HoSoUngTuyen', backref='ung_vien_ref', cascade='all, delete-orphan')

class NhaTuyenDung(db.Model):
    __tablename__ = 'nha_tuyen_dung'
    ma_nha_tuyen_dung = db.Column(db.Integer, db.ForeignKey('nguoi_dung.id', ondelete='CASCADE'), primary_key=True)
    ten_nha_tuyen_dung = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    so_dien_thoai = db.Column(db.String(20), nullable=True)
    
    # Quan hệ 1-1 với Công ty và 1-Nhiều với Tin Tuyển Dụng
    cong_ty = db.relationship('CongTy', backref='nha_tuyen_dung_ref', uselist=False, cascade='all, delete-orphan')
    tin_tuyen_dungs = db.relationship('TinTuyenDung', backref='nha_tuyen_dung_ref', cascade='all, delete-orphan')

class QuanTri(db.Model):
    __tablename__ = 'quan_tri'
    ma_quan_tri = db.Column(db.Integer, db.ForeignKey('nguoi_dung.id', ondelete='CASCADE'), primary_key=True)
    ho_ten = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# ========================================================
# 3. CÁC BẢNG LIÊN QUAN ĐẾN NHÀ TUYỂN DỤNG & ỨNG VIÊN
# ========================================================
class CongTy(db.Model):
    __tablename__ = 'cong_ty'
    ma_cong_ty = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_cong_ty = db.Column(db.String(255), nullable=False)
    ma_so_thue = db.Column(db.String(50), unique=True, nullable=True)
    mo_ta = db.Column(db.Text, nullable=True)
    dia_chi = db.Column(db.Text, nullable=True)
    ma_nha_tuyen_dung = db.Column(db.Integer, db.ForeignKey('nha_tuyen_dung.ma_nha_tuyen_dung', ondelete='CASCADE'), unique=True, nullable=False)

class TinTuyenDung(db.Model):
    __tablename__ = 'tin_tuyen_dung'
    tin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tieu_de = db.Column(db.String(255), nullable=False)
    mo_ta = db.Column(db.Text, nullable=False)
    han_nop = db.Column(db.Date, nullable=False)
    luong = db.Column(db.Integer, nullable=True)
    quyen_loi = db.Column(db.Text, nullable=True)
    ma_nha_tuyen_dung = db.Column(db.Integer, db.ForeignKey('nha_tuyen_dung.ma_nha_tuyen_dung', ondelete='CASCADE'), nullable=False)
    ma_trang_thai = db.Column(db.Integer, db.ForeignKey('trang_thai.ma_trang_thai', ondelete='RESTRICT'), nullable=False)
    
    # Quan hệ N-N với Kỹ năng và 1-Nhiều với Hồ sơ ứng tuyển
    ky_nang_yeu_caus = db.relationship('KyNang', secondary=tin_tuyen_dung_ky_nang, backref='cac_tin_tuyen_dung')
    ho_so_ung_tuyens = db.relationship('HoSoUngTuyen', backref='tin_tuyen_dung_ref', cascade='all, delete-orphan')

class CV(db.Model):
    __tablename__ = 'cv'
    ma_cv = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_cv = db.Column(db.String(255), nullable=False)
    ten_file = db.Column(db.String(255), nullable=False)
    hoc_van = db.Column(db.Text, nullable=True)
    kinh_nghiem_lam_viec = db.Column(db.Text, nullable=True)
    ma_ung_vien = db.Column(db.Integer, db.ForeignKey('ung_vien.ma_ung_vien', ondelete='CASCADE'), nullable=False)
    
    # Quan hệ N-N với Kỹ năng và 1-Nhiều với Hồ sơ ứng tuyển
    ky_nang_cos = db.relationship('KyNang', secondary=cv_ky_nang, backref='cac_cv')
    ho_so_ung_tuyens = db.relationship('HoSoUngTuyen', backref='cv_ref', cascade='all, delete-orphan')

# ========================================================
# 4. BẢNG TRUNG TÂM HO_SO_UNG_TUYEN
# ========================================================
class HoSoUngTuyen(db.Model):
    __tablename__ = 'ho_so_ung_tuyen'
    ma_ho_so = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ngay_nop = db.Column(db.DateTime, default=datetime.utcnow)
    
    ma_ung_vien = db.Column(db.Integer, db.ForeignKey('ung_vien.ma_ung_vien', ondelete='CASCADE'), nullable=False)
    tin_id = db.Column(db.Integer, db.ForeignKey('tin_tuyen_dung.tin_id', ondelete='CASCADE'), nullable=False)
    ma_cv = db.Column(db.Integer, db.ForeignKey('cv.ma_cv', ondelete='CASCADE'), nullable=False)
    ma_trang_thai = db.Column(db.Integer, db.ForeignKey('trang_thai.ma_trang_thai', ondelete='RESTRICT'), nullable=False)