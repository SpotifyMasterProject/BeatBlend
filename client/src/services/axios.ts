import axios from 'axios'
import {useAuthStore} from '@/stores/auth'
import applyCaseMiddleware from 'axios-case-converter';

const apiClient = applyCaseMiddleware(axios.create({
    baseURL: `http://${import.meta.env.VITE_LOCAL_IP_ADDRESS}:8000`
}));

apiClient.interceptors.request.use(
    (config) => {
        const authStore = useAuthStore()
        const token = authStore.token
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

export default apiClient