import axios from 'axios';
import Cookies from 'js-cookie';

const api = axios.create({
  baseURL: 'http://localhost:8001/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = Cookies.get('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const auth = {
  login: (email: string, password: string) =>
    api.post('/login', { email, password }),
  register: (name: string, email: string, password: string, role: string) =>
    api.post('/register', { name, email, password, role }),
  logout: () => api.post('/logout'),
  getUser: () => api.get('/user'),
};

export const items = {
  getAll: () => api.get('/items'),
  create: (data: any) => api.post('/items', data),
  update: (id: number, data: any) => api.put(`/items/${id}`, data),
  delete: (id: number) => api.delete(`/items/${id}`),
  get: (id: number) => api.get(`/items/${id}`),
  stokKeluar: (id: number, jumlah: number, keterangan?: string) =>
    api.post(`/items/${id}/keluar`, { jumlah, keterangan }),
};

export const stockHistories = {
  getAll: () => api.get('/stock-histories'),
  getMasuk: () => api.get('/stock-histories/masuk'),
  getKeluar: () => api.get('/stock-histories/keluar'),
};

export default api;