import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const authApi = {
    register: (data) => apiClient.post('/register', data),
    login: (data) => apiClient.post('/login', data),
};

export const jobApi = {
    getAllJobs: () => axiosClient.get('/jobs'),

    getJobById: (tin_id) => axiosClient.get(`/jobs/${tin_id}`)
};