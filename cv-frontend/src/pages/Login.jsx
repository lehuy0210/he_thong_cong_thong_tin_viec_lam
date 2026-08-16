import React, { useState } from 'react';
import { authApi } from '../services/api';
import '../css/auth.css';

export default function Login() {
    const [form, setForm] = useState({
        Username: '',
        Password: ''
    });

    const [errors, setErrors] = useState({});
    const [submitting, setSubmitting] = useState(false);
    const [result, setResult] = useState(null);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm((prev) => ({ ...prev, [name]: value }));
    };

    const validate = () => {
        const newErrors = {};
        if (!form.Username.trim()) newErrors.Username = 'Vui lòng nhập tên đăng nhập';
        if (!form.Password.trim()) newErrors.Password = 'Vui lòng nhập mật khẩu';
        return newErrors;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const formErrors = validate();
        setErrors(formErrors);

        if (Object.keys(formErrors).length > 0) return;

        try {
            setSubmitting(true);
            setResult(null);

            const res = await authApi.login(form);

            console.log("Kết quả từ Backend:", res.data);

            setResult({ ok: true, message: res.data.message || 'Đăng nhập thành công' });

            if (res.data.user) {
                localStorage.setItem('user', JSON.stringify(res.data.user));
            } else {
                console.warn("Không tìm thấy thông tin user từ Backend!");
            }

            window.location.href = '/home';

        } catch (err) {
            const msg = err.response?.data?.message || 'Lỗi kết nối đến máy chủ.';
            setResult({ ok: false, message: msg });
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="auth-container">
            <h2>Đăng Nhập</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Tên đăng nhập</label>
                    <input
                        type="text"
                        name="Username"
                        value={form.Username}
                        onChange={handleChange}
                    />
                    {errors.Username && <span className="error">{errors.Username}</span>}
                </div>

                <div className="form-group">
                    <label>Mật khẩu</label>
                    <input
                        type="password"
                        name="Password"
                        value={form.Password}
                        onChange={handleChange}
                    />
                    {errors.Password && <span className="error">{errors.Password}</span>}
                </div>

                <button type="submit" disabled={submitting}>
                    {submitting ? 'Đang kiểm tra...' : 'Đăng Nhập'}
                </button>

                {result?.ok && <p className="success">{result.message}</p>}
                {result && !result.ok && <p className="error">{result.message}</p>}
            </form>

            <footer style={{ marginTop: '20px', textAlign: 'center', color: '#666' }}>
                <small>Dự án phát triển bởi Nhóm 19</small>
            </footer>
        </div>
    );
}