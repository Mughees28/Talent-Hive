import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000", 
  headers: { "Content-Type": "application/json" },
});


API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// API.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     if (error.response && error.response.status === 401) {
//       console.error("Token expired. Redirecting to login...");
//       localStorage.removeItem("token");
//       localStorage.removeItem("user");
//       window.location.href = "/login"; 
//     }
//     return Promise.reject(error);
//   }
// );



export default API;
