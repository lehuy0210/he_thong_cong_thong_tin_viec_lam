import React from 'react';
import { Link } from 'react-router-dom';
import '../css/home.css';

export default function Home() {
    return (
        <div className="home-container">

            <header className="home-header">
                <Link to="/" className="logo">Cổng Việc Làm</Link>
                <nav className="nav-links">
                    <Link to="/login" className="btn-login">Đăng Nhập</Link>
                    <Link to="/register" className="btn-register">Đăng Ký</Link>
                </nav>
            </header>

            <main className="home-main">
                <section className="hero-section">
                    <h1>Tìm Kiếm Cơ Hội Nghề Nghiệp Mới</h1>
                    <p>Kết nối ứng viên tài năng với các nhà tuyển dụng hàng đầu một cách nhanh chóng và hiệu quả.</p>

                    <div className="search-bar">
                        <input
                            type="text"
                            placeholder="Nhập chức danh, từ khóa hoặc công ty..."
                        />
                        <button type="button">Tìm Việc Ngay</button>
                    </div>
                </section>
            </main>

            <footer className="home-footer">
                <p>&copy; 2026 Hệ Thống Tuyển Dụng. Dự án phát triển bởi Nhóm 19.</p>
            </footer>

        </div>
    );
}