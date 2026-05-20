// src/services/api.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:3000/api",
});

export const validateFiles = (files) =>
  api.post("/validate", files);

export const transferFiles = (payload) =>
  api.post("/transfer", payload);

export default api;