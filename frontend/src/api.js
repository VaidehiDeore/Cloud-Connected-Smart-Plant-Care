import axios from "axios";
const api=axios.create({baseURL:import.meta.env.VITE_API_URL||"http://127.0.0.1:8000/api",timeout:7000});
export function setToken(t){if(t)api.defaults.headers.common.Authorization=`Bearer ${t}`;else delete api.defaults.headers.common.Authorization}
export default api;
