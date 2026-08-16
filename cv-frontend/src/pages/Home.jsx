import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from '../components/Navbar';
import '../css/home.css';

export default function Home() {
    const navigate = useNavigate();

    const [jobs, setJobs] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchJobs = async () => {
            try {
                const res = await axios.get('http://localhost:5000/api/jobs');
                setJobs(res.data.jobs || res.data);
            } catch (error) {
                console.error("Lỗi khi lấy danh sách công việc:", error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchJobs();
    }, []);

    return (
        <div className="home-container">
            <Navbar />

            <main className="home-main">

                <section className="hero-banner">
                    <h1>Tìm việc làm, Tuyển dụng hiệu quả</h1>

                    <div className="search-wrapper">
                        <input
                            type="text"
                            className="search-input"
                            placeholder="Nhập vị trí tuyển dụng hoặc tên công ty bạn muốn tìm..."
                        />
                        <button className="btn-search">Tìm kiếm</button>
                    </div>
                </section>

                <section className="jobs-section">
                    <div className="jobs-header">
                        <h2>Việc làm tốt nhất</h2>
                    </div>

                    {isLoading ? (
                        <p className="loading-text">Đang tải danh sách công việc...</p>
                    ) : (
                        <div className="job-grid">
                            {jobs && jobs.length > 0 ? (
                                jobs.map((job) => (
                                    <div key={job.tin_id} className="job-card" onClick={() => navigate(`/jobs/${job.tin_id}`)}>

                                        <div className="job-card-header">
                                            <div className="company-logo">
                                                <img src={job.logo || "https://via.placeholder.com/60"} alt="Logo" />
                                            </div>
                                            <div className="job-info-main">
                                                <h3 className="job-title" title={job.tieu_de || job.title}>
                                                    {job.tieu_de || job.title}
                                                </h3>
                                                <p className="company-name">
                                                    {job.ten_cong_ty || job.companyName || 'Công ty TNHH Ẩn Danh'}
                                                </p>
                                            </div>
                                        </div>

                                        <div className="job-card-tags">
                                            <span className="tag salary-tag">{job.muc_luong || job.salary || 'Thỏa thuận'}</span>
                                            <span className="tag location-tag">{job.dia_diem || job.location || 'Toàn quốc'}</span>
                                        </div>

                                    </div>
                                ))
                            ) : (
                                <p className="empty-text">Hiện chưa có công việc nào trên hệ thống.</p>
                            )}
                        </div>
                    )}
                </section>

            </main>

            <footer className="home-footer">
                <p>&copy; 2026 Hệ Thống Tuyển Dụng. Dự án phát triển bởi Nhóm 19.</p>
            </footer>
        </div>
    );
}