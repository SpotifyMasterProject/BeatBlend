import axios from "axios";

const apiClient = axios.create({
  baseURL: 'http://localhost:8000'
})

//Placeholder for request interceptor (auth/token)

export default apiClient