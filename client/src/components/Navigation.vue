<script setup lang="ts">
import {RouterLink} from "vue-router";
</script>

<template>
  <nav class="navigation-bar">
    <RouterLink to="/">Landing Page</RouterLink>
    <RouterLink to="/home">Home</RouterLink>
    <RouterLink to="/about">About</RouterLink>
    <RouterLink to="/websockets">Websocket Test</RouterLink>
  </nav>
</template>

<style scoped>
.navigation-bar{
  display: flex;
  justify-content: center;
  gap: 1rem;
  padding: 1rem 0;
}
.nav-link{
  text-decoration: none;
  color: var(--Font-color);
  padding: 0 1rem;
  border-left: 1px solid #6BA149;
  transition: color 0.3s, background-color 0.3s;
}
.nav-link:first-of-type{
  border-left: 0;
}
.nav-link.active{
  color:#6BA149;
}
.nav-link:hover{
  color:#6BA149;
}

</style>