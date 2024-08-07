<script setup lang="ts">
import {onMounted, ref} from 'vue'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import {authService} from '@/services/authService'
import {isMobile} from '../services/layoutService'
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
  <div class="landing-view">
    <div class="login-container">
      <Button @click="redirectToSpotify" class="button spotify-button">
        Login via Spotify
      </Button>

      <div class="session-scanner">
        <Button v-if="isMobile" class="button">Scan Session QR</Button>
        <span v-else class="fallback-text">Use mobile to join Session</span>
      </div>
    </div>
  </div>
</template>

<style scoped>

.landing-view {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
.login-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  justify-items: center;
  width: 200px;
}

.button {
  padding: 8px 16px; /* Reduced padding */
  border: none;
  border-radius: 25px;
  font-size: 14px; /* Reduced font size */
  cursor: pointer;
  height: 40px;
}

.spotify-button {
  background-color: #1db954;
  color: white;
}

.session-scanner {
  display: flex;
  justify-content: center;
}

.session-scanner .button {
  background-color: #F9F9F9;
  color: black;
}

.session-scanner .fallback-text {
  color: white;
}

</style>