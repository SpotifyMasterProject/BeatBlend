<!--
TODO: This file acts as a placeholder.
TODO: It is temporary to handle the callback from the spotify auth.
TODO: It should be replaced with the home screen as soon as it is implemented.
TODO: The setup code with the onMounted hook should be carried over to the home screen file.
-->


<script setup lang="ts">
  import {authService} from "@/services/authService";
  import {onMounted} from "vue";

  const urlParams = new URLSearchParams(window.location.search)
  const code = urlParams.get('code') || 'placeholder'
  const state = urlParams.get('state')

  onMounted(async () => {
    await authService.storeAuthCode(code)
        .then((response) => {
          console.log(response)
        })
        .catch((error) => {
          console.log(error)
        })

    //TODO: not ugly response
    //TODO: spotify error catching
    //TODO: what if code does not exist? also handled via error?
  })
</script>

<template>
  <div class="spotifyAuth">
    <h1>Spotify OAuth Proof of Concept</h1>
    <h2>Callback Successful!</h2>
  </div>

</template>

<style scoped>

</style>