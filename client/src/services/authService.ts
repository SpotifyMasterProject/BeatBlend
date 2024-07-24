import apiClient from "@/services/axios";

export const authService = {
    async storeAuthCode(auth_code: string) {
        return await apiClient.post('/auth-codes', {
            auth_code: auth_code
        })
    }
}