<script setup lang="ts">
import Flower from "@/components/Flower.vue";
import {SongFeatureCategory} from '@/types/SongFeature';
import {ref, onMounted, onUnmounted} from 'vue';

const songList = ref([
  { title: "Baby Powder", artist: "Jenevieve", features: [
      { category: SongFeatureCategory.ENERGY, value: 0.4 },
      { category: SongFeatureCategory.DANCEABILITY, value: 0.6 },
      { category: SongFeatureCategory.SPEECHINESS, value: 0.5 },
      { category: SongFeatureCategory.VALENCE, value: 0.3 },
      { category: SongFeatureCategory.TEMPO, value: 0.7 }
    ]},
  { title: "Blue Moon", artist: "NIKI", features: [
      { category: SongFeatureCategory.ENERGY, value: 0.5 },
      { category: SongFeatureCategory.DANCEABILITY, value: 0.7 },
      { category: SongFeatureCategory.SPEECHINESS, value: 0.4 },
      { category: SongFeatureCategory.VALENCE, value: 0.7 },
      { category: SongFeatureCategory.TEMPO, value: 0.5 }
    ]},
  { title: "Oscar Winning Tears", artist: "RAYE", features: [
      { category: SongFeatureCategory.ENERGY, value: 0.4 },
      { category: SongFeatureCategory.DANCEABILITY, value: 0.8 },
      { category: SongFeatureCategory.SPEECHINESS, value: 0.6 },
      { category: SongFeatureCategory.VALENCE, value: 0.4 },
      { category: SongFeatureCategory.TEMPO, value: 0.7 }
    ]}
]);

const selectedVote = ref<number | null>(null);
const countdown = ref(90);
let timer: NodeJS.Timeout | null = null;

const handleVote = (songIndex: number) => {
  if (selectedVote.value === songIndex) {
    selectedVote.value = null; // Deselect the current song if clicked again
  } else {
    selectedVote.value = songIndex; // Select the song and deselect any previously selected one
  }
  console.log(`Voted for song ${songList.value[songIndex].title}`);
};

// countdown
onMounted(() => {
  timer = setInterval(() => {
    if (countdown.value > 0) {
      countdown.value -= 1;
    }
  }, 1000);
});

onUnmounted(() => {
  if (timer) {
    clearInterval(timer); // Cleanup interval when the component unmounts
  }
});

</script>

<template>
  <div class="mobile-visualization">
    <div class="sticky-header">
      <h2 class="header">Vote for the next song!</h2>
      <p class="countdown">Time remaining: {{ countdown }}s</p>
    </div>
    <div class="song-list">
      <div v-for="(song, index) in songList" :key="index" class="song-item">
        <Flower :features="song.features" :size="80" :circleRadius="40" />
        <div class="song-details">
          <p class="song-title">{{ song.title }}</p>
          <p class="song-artist">{{ song.artist }}</p>
        </div>
        <div class="vote-controls">
          <button
            :class="{ active: selectedVote === index }"
            @click="handleVote(index)"
          >
            <i class="pi pi-thumbs-up"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
.mobile-visualization {
  text-align: center;
  color: white;
  overflow: auto;
}

.sticky-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: #272525;
}

.header {
  font-size: 18px;
  margin-top: 0;
  margin-bottom: 5px;
}

.countdown {
  font-size: 16px;
  margin-bottom: 5px;
  color: #ffcc00;
}

.song-list {
  display: flex;
  flex-direction: column;
  padding-left: 5px;
}

.song-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 5px 0;
}

.song-details {
  flex: 1;
  padding-left: 5px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
}

.song-title, .song-artist {
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.vote-controls {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.vote-controls button {
  background: none;
  border: none;
  font-size: 24px;
  color: white;
  cursor: pointer;
}

.vote-controls button.active {
  color: #6AA834;
}
</style>
