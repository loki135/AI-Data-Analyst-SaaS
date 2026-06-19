import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
});

// Attach token to every request automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  // Debug: log request headers to help diagnose 401s
  try {
    // avoid circular structure issues
    const safeHeaders = { ...config.headers };
    // eslint-disable-next-line no-console
    console.log('API request', config.method, config.url, safeHeaders);
  } catch (e) {}
  return config;
});

export default api;