<script setup lang="ts">
import {ref, watch, onMounted} from 'vue';
import Navigation from "@/components/Navigation.vue";
import Flower from "@/components/Flower.vue";
import type { CSSProperties } from 'vue';
import Button from 'primevue/button';
import LogoIntroScreen from "@/components/LogoIntroScreen.vue";
import PreviouslyPlayed from "@/components/PreviouslyPlayed.vue";
import QrcodeVue from 'qrcode.vue'
import AddMoreSong from "@/components/AddMoreSong.vue";
import { HostSession } from "@/types/Session";

const showPreviouslyPlayed = ref(false);
const showAddMoreSongPopup = ref(false);

const LOCAL_IP_ADDRESS = import.meta.env.VITE_LOCAL_IP_ADDRESS;

const toggleVisibility = () => {
  showPreviouslyPlayed.value = !showPreviouslyPlayed.value;
};

// TODO: Get sessions from BE.
const sessions = [
  new HostSession({
    id: "123",
    invitationLink: `http://${LOCAL_IP_ADDRESS}/sessions/join/123`,
    guests: [],
    playlistName: "Playlist 1",
    playlist: [],
    creationDate: Date.parse("2024-03-12 12:00:20"),
    isRunning: false
  }),
  new HostSession({
    id: "234",
    invitationLink: `http://${LOCAL_IP_ADDRESS}/sessions/join/123`,
    guests: [],
    playlistName: "Playlist 2",
    playlist: [],
    creationDate: Date.parse("2024-02-12 12:00:20")
  })
];

const selectedSessionIndex = ref(0);
const toggleAddMoreSongPopup = () => {
  showAddMoreSongPopup.value = !showAddMoreSongPopup.value;
};

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
      <div class="function-icon-container">
        <Button icon="pi pi-search" severity="success" text raised rounded aria-label="Search" @click="toggleAddMoreSongPopup" />
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
    <div class="footer-section">
      <div
        class="previously-played"
        :class="{ minimized: !showPreviouslyPlayed }"
      >
        <div class="table-header-container">
          <h3>Previously Played</h3>
          <button
            class="text-sm rounded min-h-[32px] px-3 py-0.5 font-semibold hover:bg-gray-800"
            @click="toggleVisibility"
          >
            {{ showPreviouslyPlayed ? "Hide" : "Show" }}
          </button>
        </div>
        <div v-show="showPreviouslyPlayed" class="table-scroll">
          <PreviouslyPlayed></PreviouslyPlayed>
        </div>
      </div>
      <qrcode-vue :value="sessions[selectedSessionIndex].invitationLink" />
    </div>

    <!-- Popup Overlay -->
    <div v-if="showAddMoreSongPopup" class="popup-overlay" @click="toggleAddMoreSongPopup">
      <div class="popup-content" @click.stop>
        <AddMoreSong @close-popup="toggleAddMoreSongPopup"/>
      </div>
    </div>
  </div>
</template>

<style scoped>
.function-icon-container {
  position: absolute;
  top: 55px;
  left: 40px;
  z-index: 1000;
}

.function-icon-container button {
  width: 45px;
  height: 45px;
  align-items: center;
  justify-content: center;
  background-color: #6BA149;
  color: #D9D9D9;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  border-radius: 25%;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.function-icon-container button:hover {
  background-color: #6AA834;
  transform: scale(1.05);
}

.previously-played.minimized{
  height: auto;
}

.previously-played{
  background-color: var(--backcore-color1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  overflow-y: hidden;
  box-sizing: border-box;
  border-radius: 18px;
  text-align: left;
  color: #FFFFFF;
  transition: all 0.5s ease;
  max-height: 23vh;
  width: 100%;
}

.previously-played .table-header-container {
  display: flex;
  flex-direction: row;  /* Aligns the header and button horizontally */
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: #272525;
}
.previously-played.minimized .table-header-container {
  padding-bottom: 0; /* No padding when minimized */
}
.previously-played:not(.minimized) .table-header-container {
  padding-bottom: 10px; /* Adds space between the header/button and the table when shown */
}
.previously-played h3 {
  margin: 0;
  font-size:16px;
  width: 100%;
}
.previously-played button {
  padding: 8px 16px;
  background-color: #6BA149;
  color: #D9D9D9;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: background-color 0.3s ease, transform 0.2s ease;
}
.previously-played button:hover {
  background-color: #6AA834;
  transform: scale(1.05); /* Slightly enlarge the button on hover */
}
.previously-played .table-scroll {
  max-height: 700px;
  overflow-y: auto;
  overflow-x: hidden;
}

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 1000;
}

.footer-section {
  display: flex;
  flex-direction: row;
  margin: 0 20px 20px;
  gap: 8px;
  justify-content: space-between;
}
</style>
