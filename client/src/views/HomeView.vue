<script setup lang="ts">
import TheWelcome from '../components/TheWelcome.vue'
import LogoIntroScreen from "@/components/LogoIntroScreen.vue";
import { RouterLink } from 'vue-router';
import Navigation from "@/components/Navigation.vue";
</script>

<template>
  <div class="type2">
    <header>
      <div class="search-bar-background">
      <input class="search-bar" type="text" placeholder="Search" />
      </div>
      <div class="logo-nav-container">
        <logo-intro-screen/>
        <nav>
          <Navigation/>
        </nav>
      </div>

    </header>
    <div class="middle">

    </div>
    <div class="previously-played">

    </div>
  </div>
</template>
