<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import LogoIntroScreen from "@/components/LogoIntroScreen.vue";
</script>

<template>
  <div class="type2">
    <div class="type2.logo">
      <logo-intro-screen/>
    </div>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Landing Page</RouterLink>
        <RouterLink to="/home">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
        <RouterLink to="/websockets">Websocket Test</RouterLink>
      </nav>
    </div>
  </div>
  <RouterView />
</template>

<style scoped>

.type1{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  background-color: #272525;
}
header {
  margin-top: 180px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-intro-screen {
  display: block;
  margin: 0 auto;
}

.container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

header {
  line-height: 1.5;
  max-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem 0;
}


nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: #FFFFFF;
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid #6BA149;
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {

  nav {
    text-align: center;
    margin: 0;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
