<script setup lang="ts">
import {onMounted, ref} from 'vue'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import {authService} from '@/services/authService'
import LogoIntroScreen from "@/components/LogoIntroScreen.vue";
import StartBlendButton from "@/components/StartBlendButton.vue";
import Navigation from "@/components/Navigation.vue";


const username = ref<string>('')

const urlParams = new URLSearchParams(window.location.search)
const code = urlParams.get('code')
const state = urlParams.get('state')

onMounted(async () => {
  if (code != null) {
    await authService.authorizeSpotify('username_placeholder', code)
        .then((response) => {
          console.log(response)
        })
        .catch((error) => {
          console.log(error)
        })
  }
})

const redirectToSpotify = async () => {
  window.location.href = 'https://accounts.spotify.com/authorize?' +
      'response_type=' + 'code' +
      '&client_id=' + import.meta.env.VITE_SPOTIFY_CLIENT_ID +
      //'&scope' +
      '&redirect_uri=' + import.meta.env.VITE_SPOTIFY_REDIRECT_URI
      //'&state='
}

const authorize = function () {
  if (username.value === '') {
    return
  }
  authService.authorize(username.value)
      .catch((error) => {
        console.log(error)
      })
}
</script>

<template>
  <div class="type1">
    <header>
      <logo-intro-screen/>
      <nav>
        <Navigation/>
      </nav>
    </header>
    <div class="container">
      <start-blend-button />
    </div>
  </div>
</template>

<style scoped>
</style>