import axios from "axios";
import { getToken, removeToken, removeUser } from "./auth";

const API_URL = "http://localhost:8000";

// Создаем экземпляр axios с базовой конфигурацией
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor для добавления токена к каждому запросу
apiClient.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor для обработки ошибок авторизации
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Токен невалиден или отсутствует - очищаем и редиректим на логин
      removeToken();
      removeUser();
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default apiClient;

