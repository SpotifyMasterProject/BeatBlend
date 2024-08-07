<script setup lang="ts">
import LogoIntroScreen from "@/components/LogoIntroScreen.vue";
import Navigation from "@/components/Navigation.vue";
import Flower from "@/components/Flower.vue";

const flowerData = [
  { value: 0.4, color: '#144550' },
  { value: 0.6, color: '#31431E' },
  { value: 0.5, color: '#EEE8C4' },
  { value: 0.7, color: '#E4832E' },
  { value: 0.3, color: '#BB7DEC' },
]
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
      <Flower :features="flowerData" :size="300" :circleRadius="100" />
      <Flower :features="flowerData" :size="300" :circleRadius="100" />
      <Flower :features="flowerData" :size="300" :circleRadius="100" />
      <Flower :features="flowerData" :size="300" :circleRadius="100" />
      <Flower :features="flowerData" :size="300" :circleRadius="100" />
      <Flower :features="flowerData" :size="300" :circleRadius="100" />
      <Flower :features="flowerData" :size="300" :circleRadius="100" />
      <Flower :features="flowerData" :size="300" :circleRadius="100" />
      <Flower :features="flowerData" :size="300" :circleRadius="100" />
      <Flower :features="flowerData" :size="300" :circleRadius="100" />
      <Flower :features="flowerData" :size="300" :circleRadius="100" />
      <Flower :features="flowerData" :size="300" :circleRadius="100" />
      <Flower :features="flowerData" :size="300" :circleRadius="100" />
      <Flower :features="flowerData" :size="300" :circleRadius="100" />
      <Flower :features="flowerData" :size="300" :circleRadius="100" />
      <Flower :features="flowerData" :size="300" :circleRadius="100" />
      <Flower :features="flowerData" :size="300" :circleRadius="100" />
    </div>
    <div class="previously-played">

    </div>
  </div>
</template>
