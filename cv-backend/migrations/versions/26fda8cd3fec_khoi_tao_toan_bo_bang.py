"""khoi_tao_toan_bo_bang

Revision ID: xxxx
Revises: 
Create Date: 2026-06-08 ...

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'xxxx'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ==========================================
    # 1. TẠO CÁC BẢNG DANH MỤC TRƯỚC (KHÔNG PHỤ THUỘC)
    # ==========================================
    op.create_table('vai_tro',
        sa.Column('ma_vai_tro', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('ten_vai_tro', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('ma_vai_tro'),
        sa.UniqueConstraint('ten_vai_tro')
    )

    op.create_table('trang_thai',
        sa.Column('ma_trang_thai', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('ten_trang_thai', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('ma_trang_thai'),
        sa.UniqueConstraint('ten_trang_thai')
    )

    op.create_table('ky_nang',
        sa.Column('ma_ky_nang', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('ten_ky_nang', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('ma_ky_nang'),
        sa.UniqueConstraint('ten_ky_nang')
    )

    # ==========================================
    # 2. TẠO BẢNG NGƯỜI DÙNG & CÁC BẢNG KẾ THỪA
    # ==========================================
    op.create_table('nguoi_dung',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('ma_vai_tro', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['ma_vai_tro'], ['vai_tro.ma_vai_tro'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )

    op.create_table('ung_vien',
        sa.Column('ma_ung_vien', sa.Integer(), nullable=False),
        sa.Column('ho_ten', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('gioi_tinh', sa.Enum('Nam', 'Nữ'), nullable=True),
        sa.Column('so_dien_thoai', sa.String(length=20), nullable=True),
        sa.Column('ngay_sinh', sa.Date(), nullable=True),
        sa.Column('dia_chi', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['ma_ung_vien'], ['nguoi_dung.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('ma_ung_vien'),
        sa.UniqueConstraint('email')
    )

    op.create_table('nha_tuyen_dung',
        sa.Column('ma_nha_tuyen_dung', sa.Integer(), nullable=False),
        sa.Column('ten_nha_tuyen_dung', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('so_dien_thoai', sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(['ma_nha_tuyen_dung'], ['nguoi_dung.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('ma_nha_tuyen_dung'),
        sa.UniqueConstraint('email')
    )

    op.create_table('quan_tri',
        sa.Column('ma_quan_tri', sa.Integer(), nullable=False),
        sa.Column('ho_ten', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.ForeignKeyConstraint(['ma_quan_tri'], ['nguoi_dung.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('ma_quan_tri'),
        sa.UniqueConstraint('email')
    )

    # ==========================================
    # 3. TẠO CÁC BẢNG DỮ LIỆU
    # ==========================================
    op.create_table('cong_ty',
        sa.Column('ma_cong_ty', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('ten_cong_ty', sa.String(length=255), nullable=False),
        sa.Column('ma_so_thue', sa.String(length=50), nullable=True),
        sa.Column('mo_ta', sa.Text(), nullable=True),
        sa.Column('dia_chi', sa.Text(), nullable=True),
        sa.Column('ma_nha_tuyen_dung', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['ma_nha_tuyen_dung'], ['nha_tuyen_dung.ma_nha_tuyen_dung'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('ma_cong_ty'),
        sa.UniqueConstraint('ma_nha_tuyen_dung'),
        sa.UniqueConstraint('ma_so_thue')
    )

    op.create_table('tin_tuyen_dung',
        sa.Column('tin_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('tieu_de', sa.String(length=255), nullable=False),
        sa.Column('mo_ta', sa.Text(), nullable=False),
        sa.Column('han_nop', sa.Date(), nullable=False),
        sa.Column('luong', sa.Integer(), nullable=True),
        sa.Column('quyen_loi', sa.Text(), nullable=True),
        sa.Column('ma_nha_tuyen_dung', sa.Integer(), nullable=False),
        sa.Column('ma_trang_thai', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['ma_nha_tuyen_dung'], ['nha_tuyen_dung.ma_nha_tuyen_dung'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['ma_trang_thai'], ['trang_thai.ma_trang_thai'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('tin_id')
    )

    op.create_table('cv',
        sa.Column('ma_cv', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('ten_cv', sa.String(length=255), nullable=False),
        sa.Column('ten_file', sa.String(length=255), nullable=False),
        sa.Column('hoc_van', sa.Text(), nullable=True),
        sa.Column('kinh_nghiem_lam_viec', sa.Text(), nullable=True),
        sa.Column('ma_ung_vien', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['ma_ung_vien'], ['ung_vien.ma_ung_vien'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('ma_cv')
    )

    # ==========================================
    # 4. TẠO CÁC BẢNG TRUNG GIAN (N-N)
    # ==========================================
    op.create_table('ho_so_ung_tuyen',
        sa.Column('ma_ho_so', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('ngay_nop', sa.DateTime(), nullable=True),
        sa.Column('ma_ung_vien', sa.Integer(), nullable=False),
        sa.Column('tin_id', sa.Integer(), nullable=False),
        sa.Column('ma_cv', sa.Integer(), nullable=False),
        sa.Column('ma_trang_thai', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['ma_cv'], ['cv.ma_cv'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['ma_trang_thai'], ['trang_thai.ma_trang_thai'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['ma_ung_vien'], ['ung_vien.ma_ung_vien'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tin_id'], ['tin_tuyen_dung.tin_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('ma_ho_so')
    )

    op.create_table('cv_ky_nang',
        sa.Column('ma_cv', sa.Integer(), nullable=False),
        sa.Column('ma_ky_nang', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['ma_cv'], ['cv.ma_cv'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['ma_ky_nang'], ['ky_nang.ma_ky_nang'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('ma_cv', 'ma_ky_nang')
    )

    op.create_table('tin_tuyen_dung_ky_nang',
        sa.Column('tin_id', sa.Integer(), nullable=False),
        sa.Column('ma_ky_nang', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['ma_ky_nang'], ['ky_nang.ma_ky_nang'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tin_id'], ['tin_tuyen_dung.tin_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('tin_id', 'ma_ky_nang')
    )


def downgrade():
    # Phải xóa ngược từ dưới lên để không vướng khóa ngoại
    op.drop_table('tin_tuyen_dung_ky_nang')
    op.drop_table('cv_ky_nang')
    op.drop_table('ho_so_ung_tuyen')
    op.drop_table('cv')
    op.drop_table('tin_tuyen_dung')
    op.drop_table('cong_ty')
    op.drop_table('quan_tri')
    op.drop_table('nha_tuyen_dung')
    op.drop_table('ung_vien')
    op.drop_table('nguoi_dung')
    op.drop_table('ky_nang')
    op.drop_table('trang_thai')
    op.drop_table('vai_tro')