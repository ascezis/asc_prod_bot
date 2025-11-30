import axios from "axios";

const API_URL = "http://localhost:8000";

export const getStatistics = async () => {
  const res = await axios.get(`${API_URL}/statistics/`);
  return res.data;
};

