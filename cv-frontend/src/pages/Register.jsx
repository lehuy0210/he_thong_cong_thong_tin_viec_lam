import React, { useState } from 'react';
import { authApi } from '../services/api';
import '../css/auth.css';

export default function Register() {
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

            const dataToSend = {
                Username: form.Username,
                Password: form.Password,
                VaiTro: 'ung_vien'
            };

            const res = await authApi.register(dataToSend);

            setResult({ ok: true, message: res.data.message });
            setForm({ Username: '', Password: '' });

        } catch (err) {
            const msg = err.response?.data?.message || 'Lỗi kết nối đến máy chủ.';
            setResult({ ok: false, message: msg });
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="auth-container">
            <h2>Đăng Ký Tài Khoản</h2>
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
                    {submitting ? 'Đang xử lý...' : 'Đăng Ký'}
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