import axios from "axios";

const API_URL = "http://localhost:8000";

export const getProjects = async (params = {}) => {
  const res = await axios.get(`${API_URL}/projects/`, { params });
  return res.data;
};

export const getProject = async (id) => {
  const res = await axios.get(`${API_URL}/projects/${id}`);
  return res.data;
};

export const createProject = async (data) => {
  const res = await axios.post(`${API_URL}/projects/`, data);
  return res.data;
};

export const updateProject = async (id, data) => {
  const res = await axios.put(`${API_URL}/projects/${id}`, data);
  return res.data;
};

export const deleteProject = async (id) => {
  const res = await axios.delete(`${API_URL}/projects/${id}`);
  return res.data;
};
