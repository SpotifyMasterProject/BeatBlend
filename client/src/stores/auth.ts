import {defineStore} from "pinia";
import {computed, ref} from "vue";
import {User} from "@/types/User";
import router from "@/router";

export const useAuthStore = defineStore('auth', () => {
    const user = ref<User>()
    const token = ref<string>()

    const authorized = computed<boolean>(() => {
        return token.value !== undefined
    })

    const storedUserData = localStorage.getItem('user')
    const storedToken = sessionStorage.getItem('token')
    // if (storedUserData && storedToken) { //TODO: *1 investigate if needed
    if (storedToken) {
        // user.value = new User(JSON.parse(storedUserData))
        token.value = JSON.parse(storedToken)
    }

    const authorize = async function (access_token: string) {
        sessionStorage.setItem('token', JSON.stringify(access_token))
        token.value = access_token //TODO: investigate if removable after implementing get user and store details *1

        //TODO: get user and store details
        await router.push({name: 'home'})
    }

    const deauthorize = async function () {
        user.value = undefined
        token.value = undefined
        localStorage.removeItem('user')
        await router.push({name: ''})
    }

    return {
        user,
        token,
        authorized,
        authorize,
        deauthorize
    }
})