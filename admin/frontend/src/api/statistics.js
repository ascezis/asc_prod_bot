import apiClient from "./axiosConfig";

export const getStatistics = async () => {
  const res = await apiClient.get("/statistics/");
  return res.data;
};

