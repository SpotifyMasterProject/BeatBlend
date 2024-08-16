<script setup lang="ts">
import {ref,watch,onMounted} from 'vue';
import LogoIntroScreen from "@/components/LogoIntroScreen.vue";
import Navigation from "@/components/Navigation.vue";
import Flower from "@/components/Flower.vue";

// Petal and their color & value -- Adapt length not correct yet
const flowerData = ref([
  [
    { value: 0.4, color: '#144550' },
    { value: 0.6, color: '#31431E' },
    { value: 0.5, color: '#EEE8C4' },
    { value: 0.7, color: '#E4832E' },
    { value: 0.3, color: '#BB7DEC' },
  ],
  [
    { value: 0.5, color: '#144550' },
    { value: 0.7, color: '#31431E' },
    { value: 0.4, color: '#EEE8C4' },
    { value: 0.6, color: '#E4832E' },
    { value: 0.5, color: '#BB7DEC' },
  ],
  [
    { value: 0.5, color: '#144550' },
    { value: 0.4, color: '#31431E' },
    { value: 0.6, color: '#EEE8C4' },
    { value: 0.6, color: '#E4832E' },
    { value: 0.2, color: '#BB7DEC' },
  ],
  [
    { value: 0.4, color: '#144550' },
    { value: 0.8, color: '#31431E' },
    { value: 0.3, color: '#EEE8C4' },
    { value: 0.3, color: '#E4832E' },
    { value: 0.8, color: '#BB7DEC' },
  ],
  // Add more flowers as needed
]);

//Zoom Function for the main visualization --> will be adapted at a later point
//const zoomLevel = ref(1);
//const minZoom = 0.5;
//const maxZoom = 2;

//const visualizationStyle = ref({
//  transform: `scale(${zoomLevel.value})`,
//  transformOrigin: 'bottom left',
//});

//const isScrollEnabled = ref(false);

//function zoomIn() {
//  zoomLevel.value = Math.min(zoomLevel.value + 0.1, maxZoom)
//  updateZoom();
//}
//function zoomOut() {
//  zoomLevel.value = Math.max(zoomLevel.value - 0.1, minZoom);
//  updateZoom();
//}

// function updateZoom() {
//   console.log('Updating Zoom:', zoomLevel.value);
//   visualizationStyle.value.transform = `scale(${zoomLevel.value})`;
//   isScrollEnabled.value = zoomLevel.value > 1;
//   console.log('Scroll Enabled:', isScrollEnabled.value);
// }

// function adjustZoomToFitContainer() {
//   const container = document.querySelector('.visualization-container');
//   if (container) {
//     const containerWidth = container.clientWidth;
//     const containerHeight = container.clientHeight;

//     const maxFlowerSize = 200; // Adjust based on the largest flower size
//     const numFlowers = flowerData.value.length;

//     // Assuming a simple grid layout for calculating total size
//     const totalWidth = maxFlowerSize * Math.sqrt(numFlowers);
//     const totalHeight = maxFlowerSize * Math.sqrt(numFlowers);

//     const requiredZoom = Math.min(
//         containerWidth / totalWidth,
//         containerHeight / totalHeight
//     );

//     zoomLevel.value = Math.min(requiredZoom, maxZoom);
//     updateZoom();
//   }
// }

// watch(flowerData, () => {
//   const flowerCount = flowerData.value.length;

//   //needs to be adapted once layout is correct//
//   if (flowerCount > 10) {
//     zoomLevel.value = minZoom;
//     updateZoom();
//   }
// }, { immediate: true });

//Information Button to read more about how the visualization can be read
const infoVisible = ref(true);
function toggleInfo(){
  infoVisible.value = !infoVisible.value;
}

// Generate a random offset
function generateRandomOffset(range: number) {
  return Math.random() * range - range / 2;
}

// Store initial x and y for each new flower
const maxOffset = 50;
const flowerOffsets = ref(flowerData.value.map(() => ({
  x: generateRandomOffset(maxOffset),
  y: generateRandomOffset(maxOffset),
})));

//Function stores positions so they remain constant when zooming
const getFlowerStyles = (index: number) => {
  const baseSize = 200;
  //const size = baseSize * zoomLevel.value;
  const size = baseSize;

  const { x, y } = flowerOffsets.value[index];

  return {
    width: `${size}px`,
    height: `${size}px`,
    transform: `translate(${x}px, ${y}px)`,
  };
};

onMounted(() => {
  console.log('Component Mounted');
//  adjustZoomToFitContainer(); // Fit visualization to container size on mount
//  updateZoom();
});

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
      <div class="info-box" :class="{ active: infoVisible }" @click="toggleInfo">
        <div> i </div>
      </div>
      <div :class="['visualization-container']">
        <div class="visualization">
          <!-- Loop through each flower and apply the styles -->
          <div
              v-for="(flower, index) in flowerData"
              :key="index"
              :style="getFlowerStyles(index)"
              class="flower-wrapper"
          >
            <Flower
                :features="flower"
                :size="400"
                :circleRadius="80"
            />
          </div>
        </div>
      </div>
    </div>
    <div class="previously-played"></div>
  </div>
</template>

<style scoped>

</style>
