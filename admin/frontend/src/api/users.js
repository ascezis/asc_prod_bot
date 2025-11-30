import apiClient from "./axiosConfig";

// Получить список пользователей
export const getUsers = async (search = null, role = null, limit = 100, offset = 0) => {
  const params = new URLSearchParams();
  if (search) params.append("search", search);
  if (role) params.append("role", role);
  params.append("limit", limit);
  params.append("offset", offset);

  const res = await apiClient.get(`/users?${params.toString()}`);
  return res.data;
};

// Получить пользователя по ID
export const getUser = async (userId) => {
  const res = await apiClient.get(`/users/${userId}`);
  return res.data;
};

// Обновить пользователя
export const updateUser = async (userId, userData) => {
  const res = await apiClient.put(`/users/${userId}`, userData);
  return res.data;
};

// Удалить пользователя
export const deleteUser = async (userId) => {
  const res = await apiClient.delete(`/users/${userId}`);
  return res.data;
};

