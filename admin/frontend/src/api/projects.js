import apiClient from "./axiosConfig";

export const getProjects = async (params = {}) => {
  const res = await apiClient.get("/projects/", { params });
  return res.data;
};

export const getProject = async (id) => {
  const res = await apiClient.get(`/projects/${id}`);
  return res.data;
};

export const createProject = async (data) => {
  const res = await apiClient.post("/projects/", data);
  return res.data;
};

export const updateProject = async (id, data) => {
  const res = await apiClient.put(`/projects/${id}`, data);
  return res.data;
};

export const deleteProject = async (id) => {
  const res = await apiClient.delete(`/projects/${id}`);
  return res.data;
};
