import axios from "axios";

const API_URL = "http://localhost:8000";

export const getClients = async (params = {}) => {
  const res = await axios.get(`${API_URL}/clients/`, { params });
  return res.data;
};

export const getClient = async (id) => {
  const res = await axios.get(`${API_URL}/clients/${id}`);
  return res.data;
};

export const createClient = async (data) => {
  const res = await axios.post(`${API_URL}/clients/`, data);
  return res.data;
};

export const updateClient = async (id, data) => {
  const res = await axios.put(`${API_URL}/clients/${id}`, data);
  return res.data;
};

export const deleteClient = async (id) => {
  const res = await axios.delete(`${API_URL}/clients/${id}`);
  return res.data;
};

