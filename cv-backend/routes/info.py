from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os

bp = Blueprint('info', __name__, url_prefix='/info')

ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


@bp.route('/account/<int:user_id>', methods=['PUT'])
def update_account(user_id):
    """Cập nhật thông tin tài khoản. Mong đợi JSON với các trường cần cập nhật.
    Cố gắng sử dụng model SQLAlchemy NguoiDung hoặc thực thi DB thô làm dự phòng.
    """
    data = request.get_json() or {}
    if not data:
        return jsonify({'error': 'không có dữ liệu'}), 400

    # Thử dùng model SQLAlchemy
    try:
        from models import NguoiDung
        from db import db

        user = NguoiDung.query.get(user_id)
        if not user:
            return jsonify({'error': 'không tìm thấy người dùng'}), 404

        # cập nhật các trường được phép
        for k, v in data.items():
            if hasattr(user, k):
                setattr(user, k, v)

        db.session.commit()
        return jsonify({'message': 'tài khoản đã cập nhật'}), 200
    except Exception:
        # Dự phòng: SQL thô qua kết nối DB nếu có sẵn
        try:
            from db import get_db
            conn = get_db()
            # xây dựng mệnh đề SET đơn giản
            fields = []
            vals = []
            for k, v in data.items():
                fields.append(f"`{k}`=%s")
                vals.append(v)
            if not fields:
                return jsonify({'error': 'không có trường để cập nhật'}), 400
            vals.append(user_id)
            sql = f"UPDATE nguoi_dung SET {', '.join(fields)} WHERE id=%s"
            cur = conn.cursor()
            cur.execute(sql, vals)
            conn.commit()
            return jsonify({'message': 'tài khoản đã cập nhật'}), 200
        except Exception as e:
            current_app.logger.exception(e)
            return jsonify({'error': 'cập nhật thất bại'}), 500


@bp.route('/account/<int:user_id>', methods=['DELETE'])
def delete_account(user_id):
    """Xóa tài khoản. Điều này cũng sẽ xóa các bảng liên quan nếu ràng buộc cơ sở dữ liệu tồn tại."""
    try:
        from models import NguoiDung
        from db import db
        user = NguoiDung.query.get(user_id)
        if not user:
            return jsonify({'error': 'không tìm thấy người dùng'}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'tài khoản đã xóa'}), 200
    except Exception:
        try:
            from db import get_db
            conn = get_db()
            cur = conn.cursor()
            cur.execute('DELETE FROM nguoi_dung WHERE id=%s', (user_id,))
            conn.commit()
            return jsonify({'message': 'tài khoản đã xóa'}), 200
        except Exception as e:
            current_app.logger.exception(e)
            return jsonify({'error': 'xóa thất bại'}), 500


@bp.route('/account/<int:user_id>/avatar', methods=['POST'])
def upload_avatar(user_id):
    """Tải lên hoặc cập nhật ảnh đại diện của người dùng.
    Chấp nhận form-data với trường file 'avatar'. Lưu file vào UPLOAD_FOLDER được cấu hình và
    cập nhật cột 'avatar' trong bản ghi người dùng nếu tồn tại.
    """
    if 'avatar' not in request.files:
        return jsonify({'error': 'không có file'}), 400
    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'error': 'chưa chọn file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_app.config.get('UPLOAD_FOLDER', os.path.join(current_app.root_path, 'uploads'))
        os.makedirs(upload_folder, exist_ok=True)
        dest = os.path.join(upload_folder, f"user_{user_id}_" + filename)
        file.save(dest)

        # lưu đường dẫn vào DB nếu có thể
        try:
            from models import NguoiDung
            from db import db
            user = NguoiDung.query.get(user_id)
            if not user:
                return jsonify({'error': 'không tìm thấy người dùng'}), 404
            if hasattr(user, 'avatar'):
                user.avatar = dest
                db.session.commit()
            return jsonify({'message': 'ảnh đại diện đã tải lên', 'path': dest}), 200
        except Exception:
            # dự phòng: không có gì khác để làm
            return jsonify({'message': 'ảnh đại diện đã tải lên', 'path': dest}), 200
    else:
        return jsonify({'error': 'loại tệp không được phép'}), 400
