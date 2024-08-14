<script setup lang="ts">
import LogoIntroScreen from "@/components/LogoIntroScreen.vue";
import Navigation from "@/components/Navigation.vue";
import Flower from "@/components/Flower.vue";
import PreviouslyPlayed from "@/components/PreviouslyPlayed.vue";
import AddMoreSong from "@/components/AddMoreSong.vue";
import { ref, onMounted } from "vue";


const showPreviouslyPlayed = ref(false);
const showAddMoreSongPopup = ref(false);

const toggleVisibility = () => {
  showPreviouslyPlayed.value = !showPreviouslyPlayed.value;
};

const toggleAddMoreSongPopup = () => {
  showAddMoreSongPopup.value = !showAddMoreSongPopup.value;
};

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
      <input class="search-bar" type="text" placeholder="Search" @click="toggleAddMoreSongPopup"/>
      </div>
      <div class="logo-nav-container">
        <logo-intro-screen/>
        <nav>
          <Navigation/>
        </nav>
      </div>

    </header>
    <div class="middle" :class="{ expanded: !showPreviouslyPlayed }">
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

    <!-- Popup Overlay -->
    <div v-if="showAddMoreSongPopup" class="popup-overlay" @click="toggleAddMoreSongPopup">
      <div class="popup-content" @click.stop>
        <AddMoreSong @close-popup="toggleAddMoreSongPopup"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

type2. previously-played.minimized{
  height: auto;
}
.type2 .previously-played .table-header-container {
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
.type2 .previously-played.minimized .table-header-container {
  padding-bottom: 0; /* No padding when minimized */
}
.type2 .previously-played:not(.minimized) .table-header-container {
  padding-bottom: 10px; /* Adds space between the header/button and the table when shown */
}
.type2 .previously-played h3 {
  margin: 0;
  font-size:16px;
  width: 100%;
}
.type2 .previously-played button {
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
.type2 .previously-played button:hover {
  background-color: #6AA834;
  transform: scale(1.05); /* Slightly enlarge the button on hover */
}
.previously-played .table-scroll {
  max-height: 700px; /* Adjust based on your UI requirements */
  overflow-y: auto;
  overflow-x: hidden; /* Assuming you don't want horizontal scrolling */
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
  z-index: 1000;
}
</style>
