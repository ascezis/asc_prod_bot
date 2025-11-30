import apiClient from "./axiosConfig";

export const getClients = async (params = {}) => {
  const res = await apiClient.get("/clients/", { params });
  return res.data;
};

export const getClient = async (id) => {
  const res = await apiClient.get(`/clients/${id}`);
  return res.data;
};

export const createClient = async (data) => {
  const res = await apiClient.post("/clients/", data);
  return res.data;
};

export const updateClient = async (id, data) => {
  const res = await apiClient.put(`/clients/${id}`, data);
  return res.data;
};

export const deleteClient = async (id) => {
  const res = await apiClient.delete(`/clients/${id}`);
  return res.data;
};

