import axios from "axios";

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

let fastApi = axios.create({
  baseURL: apiUrl,
});

export { fastApi };
