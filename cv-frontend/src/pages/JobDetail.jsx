import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import '../css/home.css';

export default function JobDetail() {
    const { id } = useParams();
    const navigate = useNavigate();

    const [job, setJob] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchJobDetail = async () => {
            try {
                const res = await axios.get(`http://localhost:5000/api/jobs/${id}`);
                setJob(res.data.job || res.data);
            } catch (err) {
                setError("Không thể tải thông tin công việc hoặc công việc không tồn tại.");
            } finally {
                setIsLoading(false);
            }
        };

        fetchJobDetail();
    }, [id]);

    const handleApply = () => {
        alert(`Chức năng nộp CV cho công việc ${id} đang được hoàn thiện!`);
    };

    if (isLoading) return <div style={{ textAlign: 'center', marginTop: '50px' }}>Đang tải dữ liệu...</div>;
    if (error) return <div style={{ textAlign: 'center', marginTop: '50px', color: 'red' }}>{error}</div>;
    if (!job) return null;

    return (
        <div className="home-container">
            <header className="home-header">
                <Link to="/home" className="logo">Cổng Việc Làm</Link>
                <button onClick={() => navigate(-1)} style={{ padding: '8px 15px', cursor: 'pointer' }}>Quay lại</button>
            </header>

            <main className="home-main" style={{ padding: '40px 20px', maxWidth: '800px', margin: '0 auto' }}>
                <div style={{ backgroundColor: '#fff', padding: '30px', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>

                    <h1 style={{ color: '#007bff', marginBottom: '10px' }}>{job.tieu_de || job.title}</h1>
                    <h3 style={{ color: '#555', marginBottom: '20px' }}>Công ty: {job.ten_cong_ty || job.companyName || 'Đang cập nhật'}</h3>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '30px', backgroundColor: '#f8f9fa', padding: '15px', borderRadius: '5px' }}>
                        <p><strong>📍 Địa điểm:</strong> {job.dia_diem || job.location || 'Chưa rõ'}</p>
                        <p><strong>💰 Mức lương:</strong> <span style={{ color: '#d9534f', fontWeight: 'bold' }}>{job.muc_luong || job.salary || 'Thỏa thuận'}</span></p>
                        <p><strong>⏳ Hình thức:</strong> {job.hinh_thuc || job.jobType || 'Toàn thời gian'}</p>
                        <p><strong>📅 Hạn nộp:</strong> {job.han_nop || job.deadline || 'Không giới hạn'}</p>
                    </div>

                    <div style={{ marginBottom: '20px' }}>
                        <h4>Mô tả công việc:</h4>
                        <p style={{ whiteSpace: 'pre-line', lineHeight: '1.6' }}>
                            {job.mo_ta || job.description || 'Chưa có mô tả chi tiết.'}
                        </p>
                    </div>

                    <div style={{ marginBottom: '30px' }}>
                        <h4>Yêu cầu ứng viên:</h4>
                        <p style={{ whiteSpace: 'pre-line', lineHeight: '1.6' }}>
                            {job.yeu_cau || job.requirements || 'Không yêu cầu kinh nghiệm.'}
                        </p>
                    </div>

                    <button
                        onClick={handleApply}
                        style={{
                            width: '100%', padding: '15px', fontSize: '18px',
                            backgroundColor: '#28a745', color: 'white',
                            border: 'none', borderRadius: '5px', cursor: 'pointer',
                            fontWeight: 'bold'
                        }}
                    >
                        Ứng Tuyển Ngay
                    </button>

                </div>
            </main>
        </div>
    );
}