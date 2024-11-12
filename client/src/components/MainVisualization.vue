<script setup lang="ts">
import {ref, watch, onMounted, computed, nextTick, useTemplateRef} from 'vue';
import Flower from "@/components/Flower.vue";
import Recommendations from "@/components/Recommendations.vue";
import SongFeatureDialog from "@/components/SongFeatureDialog.vue";
import type { CSSProperties } from 'vue';
import Button from "primevue/button";
import { SongFeatureCategory } from '@/types/SongFeature';
import { Session } from '@/types/Session';
import SongDetailsPopUp from "@/components/SongDetailsPopUp.vue";
import { flattenPlaylist } from '@/types/Playlist';
import { sessionService, getSongFeatures, getSongFeatureCategory } from "@/services/sessionService";

const props = defineProps<{
  session: Session,
}>();

const playlist = computed(() => {
  return flattenPlaylist(props.session.playlist);
})

const flowerData = computed(() => {
  return playlist.value.map((song) => {
    return {
      features: getSongFeatures(song),
      mostSignificantFeature: getSongFeatureCategory(song.mostSignificantFeature),
      isQueued: song.isQueued
    };
  });
});

//Zoom Function for the main visualization --> will be adapted at a later point
const zoomLevel = ref(1);
const minZoom = 0.3;
const maxZoom = 3;

const visualizationStyle = ref({
  transform: `scale(${zoomLevel.value})`,
  transformOrigin: 'bottom left',
});

const isScrollEnabled = ref(false);
const flowerRefs = useTemplateRef('flowers');
const lastSongPosition = ref({});

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

    const maxFlowerSize = 240;
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

// Define a grid size and positions for flowers
const gridSize = 90;
const maxVerticalMoves = 3;
const minY = 70;

let containerWidth = 0;
let containerHeight = 0;

let lastVerticalDirection = 0;
let currentX = 0;
let currentY = Math.floor(Math.random() * gridSize * maxVerticalMoves); //Random vertical placement for the first flower
let verticalNrFlowers = 1; //Nr of flowers vertically


const generateNextRandomGridPosition = () => {
  let stayInColumn = (Math.random() > 0.5) && verticalNrFlowers <= maxVerticalMoves;
  let verticalDirection = 0;
  if (lastVerticalDirection === 1) {
      verticalDirection = 1;
  } else if (lastVerticalDirection === -1) {
    verticalDirection = -1;
  } else {
    verticalDirection = Math.random() > 0.5 ? 1 : -1;
  }
  
  if (verticalDirection === -1 && currentY <= gridSize * 2) {
    stayInColumn = false;
  }

  if (verticalDirection === 1 && currentY >= gridSize * maxVerticalMoves) {
    stayInColumn = false;
  }

  if (stayInColumn) {
    lastVerticalDirection = verticalDirection
    const verticalMove = verticalDirection * gridSize * (Math.random() > 0.5 ? 1.5 : 2);
    currentY += verticalMove;
    verticalNrFlowers++;
    return {x: currentX, y: Math.max(currentY, minY)};
  } else {
    const horizontalMove = gridSize * (Math.random() > 0.5 ? 1.5 : 2);
    currentX += horizontalMove;
    verticalNrFlowers = 1;

    lastVerticalDirection = 0;

    // Define first currentY, when moved horizontally
    const randomStartPositions = [0, gridSize * maxVerticalMoves, gridSize * Math.floor(maxVerticalMoves / 2)];
    currentY = randomStartPositions[Math.floor(Math.random() * randomStartPositions.length)];

    return { x: currentX, y: Math.max(currentY, minY)};
  }
}

// Assign positions randomly
const generateRandomGridPositions = (flowerCount: number) => {
  const positions = [];

  for (let i = 0; i < flowerCount; i++) {
    if (i == 0) {
      positions.push({ x:0, y:currentY}); // First flower starts in first column and random Y
    } else {
      positions.push(generateNextRandomGridPosition());
    }
  }

  return positions;
};

const gridPositions = ref(generateRandomGridPositions(flowerData.value.length));

const flowerPositions = computed(() => {
  for (let i = gridPositions.value.length; i < flowerData.value.length; i++) {
    gridPositions.value = [...gridPositions.value, generateNextRandomGridPosition()];
  }

  return gridPositions.value;
});

onMounted(() => {
  //Container Dimensions
  const container = document.querySelector('.visualization-container');
  if (container) {
    containerWidth = container.clientWidth;
    containerHeight = container.clientHeight;
  }

  //Zoom to fit container
  adjustZoomToFitContainer(); // Fit visualization to container size on mount
  updateZoom();

  const scrollWrapper = document.querySelector('.scroll-wrapper') as HTMLElement;
  const visualization = document.querySelector('.visualization') as HTMLElement;

  // Scroll to the bottom left
  if (scrollWrapper && visualization) {
    // Set the scroll position to the bottom
    scrollWrapper.scrollTop = scrollWrapper.scrollHeight - scrollWrapper.clientHeight;

    // Set the scroll position to the left
    scrollWrapper.scrollLeft = 0;
  }
});

const currentSelectedFeature = ref(null);
const emit = defineEmits(['flowerSelected']);
const onPetalClick = (index: number, featureCategory: SongFeatureCategory) => {
  currentSelectedFeature.value = {index, featureCategory};
  emit('flowerSelected', index, featureCategory);
};

const flowerLines = ref([]);
const localFlowerLinePositions = ref({});

const storeFlowerLinePosition = (position, index) => {
  localFlowerLinePositions.value[index] = position;
};

const globalFlowerLinePositions = (localPosition, gridPosition) => {
  if (!localPosition  || !gridPosition) {
    return null;
  }
  return {
    x: localPosition.x + gridPosition.x,
    y: localPosition.y + gridPosition.y,
  }; 
};

const curvatureRelativeIntensity = 50.0;

const shiftPoint = (a, b, p, distance) => {
    let dx = b.x - a.x;
    let dy = b.y - a.y;

    let perpendicularDx = -dy;
    let perpendicularDy = dx;

    let length = Math.sqrt(perpendicularDx * perpendicularDx + perpendicularDy * perpendicularDy);
    let unitPerpendicularDx = perpendicularDx / length;
    let unitPerpendicularDy = perpendicularDy / length;

    let newPx = p.x + unitPerpendicularDx * distance;
    let newPy = p.y + unitPerpendicularDy * distance;

    return { x: newPx, y: newPy };
};

const computeLineBetweenFlowers = (flowerA, flowerB) => {
  const convex = Math.random() > 0.5 ? 1 : -1;

  const firstCurvature = {
    x: (flowerB.x + flowerA.x) / 2,
    y: (flowerB.y + flowerA.y) / 2,
  };

  const distance = Math.abs(flowerB.x - flowerA.x) + Math.abs(flowerB.y - flowerA.y);
  const curvatureIntensity = distance * curvatureRelativeIntensity;

  const firstCurvatureShifted = shiftPoint(flowerA, flowerB, firstCurvature, curvatureRelativeIntensity);
  return `M ${flowerA.x} ${flowerA.y}
      Q ${firstCurvatureShifted.x}
        ${firstCurvatureShifted.y},
        ${flowerB.x} ${flowerB.y}`;
};

const lastFlowerPosition = ref(null);
watch(localFlowerLinePositions.value, () => { 

  flowerLines.value = []
  for (let i = 0; i < flowerData.value.length - 1; i++) {
    const currentFlower = globalFlowerLinePositions(localFlowerLinePositions.value[i], gridPositions.value[i]);
    const nextFlower = globalFlowerLinePositions(localFlowerLinePositions.value[i + 1], gridPositions.value[i + 1]);
    if (!currentFlower || !nextFlower) {
      return;
    }
    flowerLines.value.push(computeLineBetweenFlowers(currentFlower, nextFlower));
  }

  const lastPosition = localFlowerLinePositions.value[gridPositions.value.length - 1];
  if (!lastPosition) {
    return undefined;
  }

  lastFlowerPosition.value = globalFlowerLinePositions(lastPosition, gridPositions.value[gridPositions.value.length - 1]);
});

const showSongDetails = ref(false);
const hoverSong = ref(null);
const onHoverSong = (song) => {
  hoverSong.value = song;
  showSongDetails.value = true;
}
const onLeaveFlower = () => {
  showSongDetails.value = false;
}

const currentSongIndex = computed(() => {
  const currentId = props.session.playlist.currentSong.id
  console.log("current song: ", currentId)
  const currentIndex = props.session.playlist.currentSong
    ? playlist.value.findIndex(
        song => song.id === props.session.playlist.currentSong.id
      )
    : -1;
  console.log("current index: ", currentIndex)

  return currentIndex
});

const currentSongPreviewUrl = computed(() => {
  return props.session.playlist.currentSong?.previewUrl || '';
});

const audioPlayer = ref<HTMLAudioElement | null>(null);

watch(currentSongPreviewUrl, async (newUrl) => {
  if (newUrl && newUrl !== oldUrl && audioPlayer.value) {
    audioPlayer.value.pause();
    audioPlayer.value.src = newUrl;

    try {
      await audioPlayer.value.play();
    } catch (error) {
      console.warn('Autoplay failed:', error);
    }
  }
});

onMounted(() => {
  if (audioPlayer.value) {
    audioPlayer.value.autoplay = true;
  }
});
</script>

<template>
  <div id="test"></div>
  <div class = main-visualization>
    <div class="zoom-controls">
      <button @click="zoomIn">+</button>
      <button @click="zoomOut">-</button>
    </div>
    <div class= visualization-container>
      <canvas class="canvas" id="canvas" ref="canvas"></canvas>
      <div class="scroll-wrapper">
        <div v-if="!currentSongPreviewUrl" class="audio-unavailable-message">
          Current song audio not available
        </div>
        <div class="visualization" :style="visualizationStyle">
          <!-- Loop through each flower and apply the styles -->
          <svg class="svg-container" width="100vw" height="100vh">
              <Flower
                  ref="flowers"
                  v-for="(flower, index) in flowerData"
                  :key="index"
                  :features="flower.features"
                  :bloom="index === currentSongIndex"
                  :mostSignificantFeature="flower.mostSignificantFeature"
                  :circleRadius="40"
                  :position="flowerPositions[index]"
                  :class="{queued: flower.isQueued}"
                  @onPetalClick="(category) => onPetalClick(index, category)"
                  @hover="() => onHoverSong(playlist[index])"
                  @leave="onLeaveFlower"
                  @significantFeaturePosition="(position) => storeFlowerLinePosition(position, index)"
              />
              <path
                v-for="line in flowerLines"
                class="connecting-path"
                :d="line" stroke="white" fill="transparent"
              />
               <Recommendations
                v-if="session.isRunning && session.recommendations && session.playlist.queuedSongs.length === 0"
                :recommendations="session.recommendations"
                :lastFlowerPosition="lastFlowerPosition"
                @hover="(song) => onHoverSong(song)"
                @leave="onLeaveFlower"
              />
          </svg>
        </div>
      </div>
      <audio ref="audioPlayer" :src="currentSongPreviewUrl" autoplay />
      <SongDetailsPopUp v-if="showSongDetails && hoverSong" :song="hoverSong" />
    </div>
  </div>
</template>

<style scoped>
.main-visualization {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.visualization-container{
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.visualization {
  display: grid;
  grid-template-columns: repeat(auto-fill, 80px);
  grid-template-rows: repeat(auto-fill, 80px);
  width: 100%;
  height: 100%;
  position: relative;
  overflow: visible;
}

.scroll-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  right: 30px;
  bottom: 0;
  overflow-x: auto;
  overflow-y: auto;
  padding-left: 10px;
  padding-bottom: 10px;
}

.type2 .scroll-wrapper::-webkit-scrollbar {
  width: 5px;
  height: 5px;
  background-color: var(--backcore-color2);
  border-radius: 12px;
}

.type2 .scroll-wrapper::-webkit-scrollbar-thumb {
  background-color: var(--backcore-color3);
  border-radius: 12px;
}

.type2 .scroll-wrapper::-webkit-scrollbar-thumb:hover {
  background-color: var(--backcore-color1);
}

.type2 .scroll-wrapper::-webkit-scrollbar-corner {
  background-color: var(--backcore-color1);
}

.type2 .zoom-controls {
  position: absolute;
  top: 40px;
  right: 10px;
  z-index: 10;
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.type2 .zoom-controls button {
  width: 20px;
  height: 20px;
  background-color: var(--backcore-color2);
  color: var(--font-color);
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.flower {
  transition: all 0.3s ease;
}
.flower-wrapper {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 160px;
  height: 160px;
  transform: translate(-50%, -50%);
}
.recommendations {
  position: relative;
  transform: translate(0%, -50%);
  transition: all 0.3s ease;
  margin: auto;
}
.audio-unavailable-message {
  position: absolute;
  top: 10px;
  color: red;
  font-size: 1.2em;
  font-weight: bold;
  text-align: left;
  width: 100%;
  z-index: 1000;
}
.svg-container {
  position: absolute;
}
.connecting-path {
  pointer-events: none;
}
.queued {
  opacity: 0.3;
}
</style>
