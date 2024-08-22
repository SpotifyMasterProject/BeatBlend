<script setup lang="ts">
import {ref, watch, onMounted} from 'vue';
import LogoIntroScreen from "@/components/LogoIntroScreen.vue";
import Navigation from "@/components/Navigation.vue";
import Flower from "@/components/Flower.vue";
import type { CSSProperties } from 'vue';

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
const zoomLevel = ref(1);
const minZoom = 0.5;
const maxZoom = 2;

const visualizationStyle = ref({
  transform: `scale(${zoomLevel.value})`,
  transformOrigin: 'center left',
});

const isScrollEnabled = ref(false);

function zoomIn() {
  zoomLevel.value = Math.min(zoomLevel.value + 0.1, maxZoom)
  updateZoom();
}
function zoomOut() {
  zoomLevel.value = Math.max(zoomLevel.value - 0.1, minZoom);
  updateZoom();}

function updateZoom() {
  console.log('Updating Zoom:', zoomLevel.value);

  if (zoomLevel.value <1){
    visualizationStyle.value.transformOrigin = 'bottom left';
  } else {
    visualizationStyle.value.transformOrigin = 'top left';
  }

  visualizationStyle.value.transform = `scale(${zoomLevel.value})`;
  isScrollEnabled.value = zoomLevel.value > 1;

}
function adjustZoomToFitContainer() {
  const container = document.querySelector('.visualization-container');
  if (container) {
    const containerWidth = container.clientWidth;
    const containerHeight = container.clientHeight;

    const maxFlowerSize = 200; // Adjust based on the largest flower size
    const numFlowers = flowerData.value.length;

    // Assuming a simple grid layout for calculating total size
    const totalWidth = maxFlowerSize * Math.sqrt(numFlowers);
    const totalHeight = maxFlowerSize * Math.sqrt(numFlowers);

    const requiredZoom = Math.min(
        containerWidth / totalWidth,
        containerHeight / totalHeight
    );

    zoomLevel.value = Math.min(requiredZoom, maxZoom);
    updateZoom();

    if (zoomLevel.value === minZoom) {
      (visualizationStyle.value as any).left = '0px';
      (visualizationStyle.value as any).bottom = '0px';
    }
  }
}

 watch(flowerData, () => {
   const flowerCount = flowerData.value.length;

   //needs to be adapted once layout is correct//
   if (flowerCount > 10) {
     zoomLevel.value = minZoom;
     updateZoom();
   }
 }, { immediate: true });

//Information Button to read more about how the visualization can be read
const infoVisible = ref(true);
function toggleInfo(){
  infoVisible.value = !infoVisible.value;
}

// Define a grid size and positions for flowers
const gridSize = 80;
const maxVerticalMoves = 3;

let containerWidth = 0;
let containerHeight = 0;

onMounted(() => {
  const container = document.querySelector('.visualization-container');
  if (container) {
    containerWidth = container.clientWidth;
    containerHeight = container.clientHeight;
  }
});

// Assign positions randomly
const generateRandomGridPositions = (flowerCount: number) => {
  const positions = [];
  let currentX = 0;
  let currentY = Math.floor(Math.random() * gridSize * maxVerticalMoves); //Random vertical placement for the first flower
  let verticalNrFlowers = 1; //Nr of flowers vertically
  let lastVerticalDirection = 0;

  for (let i = 0; i < flowerCount; i++) {
    if (i == 0) {
      positions.push({ x:0, y:currentY}); // First flower starts in first column and random Y
    } else {
      const stayInColumn = Math.random() > 0.5; //Decide whether to stay in same column or move to right
      const maxStack = (currentY <= gridSize || currentY >= gridSize * (maxVerticalMoves-1)) ? 3 : 2; // Determine maximum vertical based on currentY position

      if (stayInColumn && verticalNrFlowers < maxStack) {
        let verticalDirection = lastVerticalDirection;

        if (lastVerticalDirection === 1) {
          verticalDirection = 1;
        } else if (lastVerticalDirection === -1) {
          verticalDirection = -1;
        } else {
          if (currentY <= gridSize) { // If currentY too close to top, next flower will be placed down
            verticalDirection = 1;
          } else if (currentY >= gridSize * maxVerticalMoves) { // If currentY too close to bottom, next flower will be placed up
            verticalDirection = -1;;
          } else {
            verticalDirection = Math.random() > 0.5 ? 1 : -1;
          }
        }
        lastVerticalDirection = verticalDirection
        const verticalMove = verticalDirection * gridSize * (Math.random() > 0.5 ? 1.5 : 2);
        currentY += verticalMove;
        verticalNrFlowers++;
        positions.push({x: currentX, y: currentY});
      } else {
        verticalNrFlowers = 0;
        const horizontalMove = gridSize * (Math.random() > 0.5 ? 1.5 : 2);
        currentX += horizontalMove;
        verticalNrFlowers = 1;

        lastVerticalDirection = 0;

        // Define first currentY, when moved horizontally
        const randomStartPositions = [0, gridSize * maxVerticalMoves, gridSize * Math.floor(maxVerticalMoves / 2)];
        currentY = randomStartPositions[Math.floor(Math.random() * randomStartPositions.length)];

        positions.push({ x: currentX, y: currentY });
      }
    }
  }

  return positions;
};

const gridPositions = ref(generateRandomGridPositions(flowerData.value.length));


// Function to calculate styles for each flower based on grid positions
const getFlowerStyles = (index: number): CSSProperties => {
  const position = gridPositions.value[index];

  if (!position) {
    console.error(`Position for flower at index ${index} is undefined.`);
    return {
      position: 'absolute',
      left: `0px`,
      top: `0px`,
      width: `160px`,
      height: `160px`,
    };
  }

  const { x, y } = position;

  return {
    position: 'absolute',
    left: `${x + 40}px`,
    top: `${y + 40}px`,
    width: `160px`,
    height: `160px`,
  };
};

onMounted(() => {
  adjustZoomToFitContainer(); // Fit visualization to container size on mount
  updateZoom();
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
      <div class="zoom-controls">
        <button @click="zoomIn">+</button>
        <button @click="zoomOut">-</button>
      </div>
      <div class="visualization-container" >
        <div class = "scroll-wrapper">
          <div class="visualization" :style="visualizationStyle">
            <!-- Loop through each flower and apply the styles -->
            <div
                v-for="(flower, index) in flowerData"
                :key="index"
                :style="getFlowerStyles(index)"
                class="flower-wrapper"
            >
              <Flower
                  :features="flower"
                  :size="80"
                  :circleRadius="40"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="previously-played"></div>
  </div>
</template>

<style scoped>

</style>
