import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import '../css/navbar.css';

export default function Navbar() {
    const [user, setUser] = useState(null);
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const menuRef = useRef(null);

    useEffect(() => {
        const userData = localStorage.getItem('user');
        if (userData) {
            try {
                setUser(JSON.parse(userData));
            } catch (error) {
                console.error("Lỗi khi đọc dữ liệu user", error);
            }
        }

        const handleClickOutside = (event) => {
            if (menuRef.current && !menuRef.current.contains(event.target)) {
                setIsMenuOpen(false);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('user');
        setUser(null);
        window.location.href = '/';
    };

    return (
        <header className="home-header">

            <div className="nav-left">
                <Link to="/home" className="logo">Cổng Việc Làm</Link>

                {user && (
                    <nav className="main-menu">
                        <Link to="/cv-manage" className="nav-item">Quản lý CV</Link>
                    </nav>
                )}
            </div>

            <div className="nav-right">
                {user ? (
                    <div className="user-menu-container" ref={menuRef}>
                        <div
                            className="user-menu-trigger"
                            onClick={() => setIsMenuOpen(!isMenuOpen)}
                        >
                            Chào, <strong>{user.Username || user.username || 'User'}</strong>
                            <span className="dropdown-arrow">▼</span>
                        </div>

                        {isMenuOpen && (
                            <div className="user-dropdown-menu">
                                <Link to="/profile" onClick={() => setIsMenuOpen(false)}>
                                    Thông tin cá nhân
                                </Link>
                                <div className="menu-divider"></div>
                                <button onClick={handleLogout} className="dropdown-logout">
                                    Đăng xuất
                                </button>
                            </div>
                        )}
                    </div>
                ) : (
                    <>
                        <Link to="/login" className="btn-login">Đăng Nhập</Link>
                        <Link to="/register" className="btn-register">Đăng Ký</Link>
                    </>
                )}
            </div>

        </header>
    );
}