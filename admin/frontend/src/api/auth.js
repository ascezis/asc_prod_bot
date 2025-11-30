import axios from "axios";

const API_URL = "http://localhost:8000";

// Функции для работы с токеном
export const getToken = () => localStorage.getItem("auth_token");
export const setToken = (token) => localStorage.setItem("auth_token", token);
export const removeToken = () => localStorage.removeItem("auth_token");
export const getUser = () => {
  const userStr = localStorage.getItem("auth_user");
  return userStr ? JSON.parse(userStr) : null;
};
export const setUser = (user) => localStorage.setItem("auth_user", JSON.stringify(user));
export const removeUser = () => localStorage.removeItem("auth_user");

// Вход в систему
export const login = async (username, password) => {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const res = await axios.post(`${API_URL}/auth/login`, formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  if (res.data.access_token) {
    setToken(res.data.access_token);
    setUser(res.data.user);
  }

  return res.data;
};

// Выход из системы
export const logout = () => {
  removeToken();
  removeUser();
};

// Получить информацию о текущем пользователе
export const getCurrentUser = async () => {
  const token = getToken();
  if (!token) return null;

  const res = await axios.get(`${API_URL}/auth/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return res.data;
};

