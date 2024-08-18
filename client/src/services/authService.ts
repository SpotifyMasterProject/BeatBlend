import apiClient from '@/services/axios'
import {useAuthStore} from '@/stores/auth'

export const authService = {
    async authorize(username: string) {
        await apiClient.post('/token', {
            username: username
        }).then(async (response) => {
            await storeAuthorization(response.data?.['accessToken'])
            console.log('Logged in as guest with username: ' + username)
        })
    },

    async authorizeSpotify(authCode: string) {
        await apiClient.post('/auth-codes', {
            authCode
        }).then(async (response) => {
            await storeAuthorization(response.data?.['accessToken'], /* isHost= */true)
            console.log('Logged in via spotify with username')
        })
    }
}

const storeAuthorization = async function (token: string, isHost = false) {
    const authStore = useAuthStore()

    if (token === undefined) {
        throw new Error('Authorization response did not include an access token.')
    }
    await authStore.authorize(token, isHost)
}