<script setup lang="ts">
import {ref,watch} from 'vue';
import LogoIntroScreen from "@/components/LogoIntroScreen.vue";
import Navigation from "@/components/Navigation.vue";
import Flower from "@/components/Flower.vue";

// Petal and their color & value -- Adapt length not correct yet
const flowerData  = ref ([
  { value: 0.4, color: '#144550' },
  { value: 0.6, color: '#31431E' },
  { value: 0.5, color: '#EEE8C4' },
  { value: 0.7, color: '#E4832E' },
  { value: 0.3, color: '#BB7DEC' },
]);

//Zoom Function for the main visualization
const zoomLevel = ref(1);
const minZoom = 0.5;
const maxZoom = 2;
const visualizationStyle = ref({
  transform: `scale(${zoomLevel.value})`,
  transformOrigin: 'bottom left',
});
const isScrollEnabled = ref(false);

function zoomIn() {
  zoomLevel.value = Math.min(zoomLevel.value + 0.1, maxZoom)
  updateZoom();
}
function zoomOut() {
  zoomLevel.value = Math.max(zoomLevel.value - 0.1, minZoom);
  updateZoom();
}

function updateZoom(){
  visualizationStyle.value.transform = `scale(${zoomLevel.value})`;
  isScrollEnabled.value = zoomLevel.value >1;
}
watch(flowerData, () => {
  const flowerCount = flowerData.value.length;

  //needs to be adapted once layout is correct//
  if (flowerCount > 10) {
    zoomLevel.value = Math.max(zoomLevel.value - 0.1, minZoom);
    updateZoom();
  }
}, { immediate: true });

const infoVisible = ref(true);
function toggleInfo(){
  infoVisible.value = !infoVisible.value;
}
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
      <div
          class="info-box"
          :class="{ active: infoVisible }"
          @click="toggleInfo"
      >
        <div> i </div>
      </div>
      <div class="visualization-container" >
        <div class ="zoom-controls">
          <button @click="zoomIn">+</button>
          <button @click="zoomOut">-</button>
        </div>
        <div class ="visualization" :style="visualizationStyle">
            <Flower v-for="(flower, index) in Array(11).fill(flowerData)" :key="index" :features="flower" :size="300" :circleRadius="100" />
        </div>
      </div>
    </div>
    <div class="previously-played">
    </div>
  </div>
</template>
