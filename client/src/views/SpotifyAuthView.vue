<script setup lang="ts">
  const client = import.meta.env.VITE_SPOTIFY_CLIENT_ID
  const redirect = import.meta.env.VITE_SPOTIFY_REDIRECT_URI

  const redirectToSpotify = async () => {
    window.location.href = 'https://accounts.spotify.com/authorize?' +
        'response_type=' + 'code' +
        '&client_id=' + client +
        //'&scope' +
        '&redirect_uri=' + redirect
        //'&state='
  }
</script>

<template>
  <div class="spotifyAuth">
    <h1>Spotify OAuth Proof of Concept</h1>
    <p>Client ID: <span v-html="client"></span></p>
    <p>Redirect URI: <span v-html="redirect"></span></p>
    <button @click="redirectToSpotify">Redirect to Spotify OAuth</button>
  </div>

</template>

<style scoped>

</style>