import apiClient from '@/services/axios'
import { useAuthStore } from '@/stores/auth'

export const userService = {
    async fetchUser() {
        await apiClient.get('/', {
        }).then(async (response) => {
            const authStore = useAuthStore();

            authStore.user = {
                ...authStore.user,
                ...response.data
            };
        })
    },
}