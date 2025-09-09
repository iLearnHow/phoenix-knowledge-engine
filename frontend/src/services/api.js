import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`Response from ${response.config.url}:`, response.status);
    return response;
  },
  (error) => {
    console.error('Response error:', error);
    if (error.response) {
      // Server responded with error status
      console.error('Error data:', error.response.data);
    } else if (error.request) {
      // Request was made but no response received
      console.error('No response received:', error.request);
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// API functions
export const contentAPI = {
  // Generate content
  generateContent: async (data) => {
    const response = await api.post('/generate/', data);
    return response.data;
  },
  
  // Get learning objectives
  getLearningObjectives: async (params = {}) => {
    const response = await api.get('/learning-objectives/', { params });
    return response.data;
  },
  
  // Get learning objective detail
  getLearningObjective: async (id) => {
    const response = await api.get(`/learning-objectives/${id}/`);
    return response.data;
  },
  
  // Validate content
  validateContent: async (data) => {
    const response = await api.post('/validate/', data);
    return response.data;
  },
  
  // Get system stats
  getStats: async () => {
    const response = await api.get('/stats/');
    return response.data;
  },
  
  // Health check
  healthCheck: async () => {
    const response = await api.get('/health/');
    return response.data;
  },
};

export default api;
