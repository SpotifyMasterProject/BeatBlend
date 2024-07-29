import apiClient from '@/services/axios'
import {useAuthStore} from '@/stores/auth'

export const authService = {
    async authorize(username: string) {
        await apiClient.post('/token', {
            username: username
        }).then(async (response) => {
            await storeAuthorization(response.data?.['access_token'])
            console.log('Logged in as guest with username: ' + username)
        })
    },

    async authorizeSpotify(username: string, auth_code: string) {
        await apiClient.post('/auth-codes', {
            username: username,
            auth_code: auth_code
        }).then(async (response) => {
            await storeAuthorization(response.data?.['access_token'])
            console.log('Logged in via spotify with username: ' + username)
        })
    }
}

const storeAuthorization = async function (token: string) {
    const authStore = useAuthStore()

    if (token === undefined) {
        throw new Error('Authorization response did not include an access token.')
    }
    await authStore.authorize(token)
}