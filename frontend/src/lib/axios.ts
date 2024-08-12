import axios from "axios";

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

let fastApi = axios.create({
  baseURL: apiUrl,
});

// create interceptor to add token
fastApi.interceptors.request.use((config) => {
  // const token = localStorage.getItem("token");
  const token = "12345";
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export { fastApi };
