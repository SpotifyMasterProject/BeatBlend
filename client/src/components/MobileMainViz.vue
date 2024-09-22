<script setup lang="ts">
import Flower from "@/components/Flower.vue";
import {SongFeatureCategory} from '@/types/SongFeature';
import {ref} from 'vue';

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

const votes = ref(songList.value.map(() => ({ up: false, down: false })));

const handleVote = (type: 'up' | 'down', songIndex: number) => {
  if (type === 'up') {
    votes.value[songIndex].up = true;
    votes.value[songIndex].down = false; // Prevents both upvote and downvote being active simultaneously
  } else if (type === 'down') {
    votes.value[songIndex].up = false;
    votes.value[songIndex].down = true;
  }
  console.log(`Voted ${type} for song ${songList.value[songIndex].title}`);
};
</script>

<template>
  <div class="mobile-visualization">
    <h2>Vote for the next song!</h2>
    <div class="song-list">
      <div v-for="(song, index) in songList" :key="index" class="song-item">
        <Flower :features="song.features" :size="80" :circleRadius="40" />
        <div class="song-details">
          <p class="song-title">{{ song.title }}</p>
          <p class="song-artist">{{ song.artist }}</p>
        </div>
        <div class="vote-controls">
          <button
            :class="{ active: votes[index].up }"
            @click="handleVote('up', index)"
          >
            <i class="pi pi-thumbs-up"></i>
          </button>
          <button
            :class="{ active: votes[index].down }"
            @click="handleVote('down', index)"
          >
            <i class="pi pi-thumbs-down"></i>
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
  gap: 10px;
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
