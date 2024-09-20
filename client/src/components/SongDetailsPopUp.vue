<template>
  <div v-if="isVisible" class="song-detail-modal">
    <div class="modal-content">
      <div class="modal-header">
        <h3>{{ song.trackName }}</h3>
        <button @click="closeModal">X</button>
      </div>
      <p><strong>Artist: </strong> {{ song.artists.join(', ') }}</p>
      <p><strong>Album: </strong> {{ song.album }}</p>
      <p><strong>Release Date: </strong> {{ song.release_date }}</p>
      <p><strong>Duration: </strong> {{ song.duration }}</p>
      <p><strong>Genre: </strong> {{ song.genre }}</p>
      <div class="popularity">
        <p><strong>Popularity: {{ song.popularity }}</strong> </p>
        <input type="range" min="0" max="100" :value="song.popularity" disabled>
        <div class="range-labels">
          <span>0</span>
          <span>100</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  song: Object,
  isVisible: Boolean,
});

const emit = defineEmits(['close']);

const closeModal = () => {
  emit('close');
};
</script>

<style scoped>
.song-detail-modal {
  position: fixed;
  top: 65%;
  left: 20%;
  transform: translate(-50%, -50%);
  background-color: #272525;
  border-radius: 15px;
  padding: 10px;
  z-index: 1001;
  width: 300px;
  color: #D9D9D9;
  border: 2px solid #6AA834;
}

.modal-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 0px 20px 0px;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
}

.modal-header button {
  background-color: transparent;
  border: none;
  color: #D9D9D9;
  font-size: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.modal-header button:hover {
  background-color: #575252;
  transform: scale(1.05);
}

p {
  margin: 0;
  font-size: 16px;
}

.popularity{
  padding-top: 10px;
}

input[type="range"] {
  width: 100%;
  -webkit-appearance: none;
  appearance: none;
  height: 4px;
  border-radius: 5px;
  outline: none;
  position: relative;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #6AA834;
  cursor: pointer;
  position: relative;
  border: none;
}

input[type="range"]::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #6AA834;
  cursor: pointer;
  position: relative;
  border: none;
}

input[type="range"]:disabled::-webkit-slider-thumb, input[type="range"]:disabled::-moz-range-thumb {
  background: #6AA834;
  border: none;
}

input[type="range"]:disabled {
  background: linear-gradient(to right, #FFFFFF, #828282);
}

.range-labels {
  display: flex;
  justify-content: space-between;
}

.range-labels span {
  font-size: 12px;
  color: #D9D9D9;
}
</style>