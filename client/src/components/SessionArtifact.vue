<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Flower from '@/components/Flower.vue';
import Button from 'primevue/button';

const defaultFlowerData = [
  { category: 'SPEECHINESS', value: 0.6 },
  { category: 'DANCEABILITY', value: 0.8 },
  { category: 'TEMPO', value: 0.7 },
  { category: 'VALENCE', value: 0.5 },
  { category: 'ENERGY', value: 0.75 },
];

const artifactDetails = {
  songsPlayed: 120,
  songsAddedManually: 30,
  genreStart: 'Pop',
  genreEnd: 'Rock',
  mostSongsAddedBy: 'User123',
  mostVotesBy: 'User456',
  firstRecommendationVotePercentage: 70,
  mostSignificantFeatureOverall: 'Danceability'
};

const hoverFeature = ref(null);

const handleHover = (feature) => {
  hoverFeature.value = feature;
};

const emit= defineEmits(['close']);
const showPopup = ref(true);
const closePopup = () => {
  emit('close');
};
</script>

<template>
  <div v-if="showPopup" class="popup-overlay">
    <div class="popup-content" >
      <header class="popup-header">
        <h2>Your Session Artifact</h2>
        <Button icon="pi pi-times" @click="closePopup" class="close-button" />
      </header>
      <div class="middle-box">
        <div class="flower-placeholder">
          <p>Flower Visualization Placeholder</p>
        </div>
      </div>
      <div class="overview-section">
        <h3>Overview</h3>
        <div class="overview-content">
          <!-- Left Column -->
          <div class="overview-left">
            <p><strong>Audio Features Ranked</strong></p>
            <ol>
              <li>Speechability</li>
              <li>Danceability</li>
              <li>Tempo</li>
              <li>Valence</li>
              <li>Energy</li>
            </ol>
            <p class="overview-comment">
              You agreed <span class="highlight">XYZ</span> with the recommendation model by choosing the first recommendation
            </p>
          </div>
          <div class="overview-right">
            <p>You played <span class="highlight">XXX</span> songs</p>
            <p>Of those, you added <span class="highlight">XXX</span> manually</p>
            <p>You started with genre <span class="highlight">XXX</span> and ended with <span class="highlight">XXX</span></p>
            <p><span class="highlight">XXX</span> added the most songs</p>
            <p><span class="highlight">XXX</span> voted most</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

.popup-content {
  background-color: var(--backcore-color1);
  color: white;
  padding: 20px;
  border-radius: 10px;
  width: 600px;
  text-align: left;
  position: relative;
}

.popup-header {
  display: flex;
  align-items: center;
  padding: 10px 0;
  margin-bottom: 30px;

}

.popup-header h2 {
  font-size: 24px;
  font-weight:bold;
  margin-bottom: -30px;
  color: #6BA149;
}

.close-button {
  margin-left: auto;
  background: none;
  border: none;
  cursor: pointer;
  color: white;
  font-size: 18px;
}

.middle-box {
  background-color: #444;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  margin-bottom: 20px;
  height: 250px;
}

.flower-placeholder {
  font-size: 14px;
  color: #888;
}


.overview-section {
  color: white;
}

.overview-section h3 {
  color: white;
  margin-bottom: 10px;
  margin-left:10px;
}

.overview-content {
  display: flex;
  justify-content: flex-start;
  margin-top: 10px;
  margin-left:10px;
}

.overview-left {
  width: 50%;
  padding-right: 20px;
  position: relative;
}

.overview-left ol::after {
  content: "";
  display: block;
  width: 80%;
  margin: 20px auto;
  border-top: 1px solid #666;
  transform: translateX(-10%);
}

.overview-comment {
  width: 90%;
  margin-top: 10px;
  font-size: 14px;
  color: white;
  text-align: center;
}

.overview-right {
  width: 50%;
  font-size: 14px;
  padding-left: 20px;
  border-left: 1px solid #666;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.overview-right::before {
  content: "";
  position: absolute;
  left: 0;
  top: 20%;
  bottom: 20%;
  width: 1px;
  height: 60%;
  transform: translateX(-50%);
}

.highlight {
  color: #6BA149;
  font-weight: bold;
}
</style>