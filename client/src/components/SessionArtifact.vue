<script setup lang="ts">
import {ref, computed, defineProps, defineEmits} from 'vue';
import Flower from '@/components/Flower.vue';
import Button from 'primevue/button';
import { useSession } from '@/stores/session';
import { SongFeature, SongFeatureCategory } from '@/types/SongFeature';


const sessionStore = useSession();

const artifactDetails = computed(() => sessionStore.session?.artifacts || {});

const props = defineProps({
  artifactData: {
    type: Object,
    required: true,
  }
});

const flowerData = computed<SongFeature[]>(() => {
  if (props.artifactData?.averageFeatures) {
    const data = [
      { category: SongFeatureCategory.SPEECHINESS, value: props.artifactData.averageFeatures.speechiness },
      { category: SongFeatureCategory.DANCEABILITY, value: props.artifactData.averageFeatures.danceability },
      { category: SongFeatureCategory.TEMPO, value: props.artifactData.averageFeatures.tempo },
      { category: SongFeatureCategory.VALENCE, value: props.artifactData.averageFeatures.valence },
      { category: SongFeatureCategory.ENERGY, value: props.artifactData.averageFeatures.energy },
    ];
    console.log("Computed flowerData for Session Artifact:", data);  // Debugging line
    return data;
  }
  return [];
});

const categoryMap: Record<SongFeatureCategory, string> = {
  [SongFeatureCategory.SPEECHINESS]: 'Speechability',
  [SongFeatureCategory.DANCEABILITY]: 'Danceability',
  [SongFeatureCategory.TEMPO]: 'Tempo',
  [SongFeatureCategory.VALENCE]: 'Valence',
  [SongFeatureCategory.ENERGY]: 'Energy',
};

//Sort ranking audio features
const sortedFeatures = computed(() => {
  return flowerData.value
      .map(feature => ({
        ...feature,
        category: categoryMap[feature.category] || feature.category // Map category to readable name
      }))
      .sort((a, b) => b.value - a.value);
});

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
          <div v-if="flowerData && flowerData.length > 0">
            <Flower :features="flowerData" />
          </div>
          <div v-else>
            <p>No data available for the flower visualization.</p>
          </div>
        </div>
      </div>
      <div class="overview-section">
        <h3>Overview</h3>
        <div class="overview-content">
          <!-- Left Column -->
          <div class="overview-left">
            <strong>Audio Features Ranked</strong>
            <ol>
              <li v-for="feature in sortedFeatures" :key="feature.category">
                {{ feature.category }} ({{ feature.value.toFixed(2) }})
              </li>
            </ol>
            <p class="overview-comment">
              You agreed <span class="highlight">XYZ</span> with the recommendation model by choosing the first recommendation
            </p>
          </div>
          <div class="overview-right">
            <p>You played <span class="highlight">{{ artifactDetails.songsPlayed }}</span> songs</p>
            <p>Of those, you added <span class="highlight">{{ artifactDetails.songsAddedManually }}</span> manually</p>
            <p>You started with genre <span class="highlight">{{ artifactDetails.genreStart }}</span> and ended with <span class="highlight">{{ artifactDetails.genreEnd }}</span></p>
            <p><span class="highlight">{{ artifactDetails.mostSongsAddedBy }}</span> added the most songs</p>
            <p><span class="highlight">{{ artifactDetails.mostVotesBy }}</span> voted most</p>
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

@media (max-height: 780px) {
  .popup-content {
    transform: scale(0.9);
    max-width: 100%;
    max-height: 100%;
    padding: 15px;
  }

  .popup-header h2 {
    font-size: 22px;
    transition: font-size 0.5s ease;
  }

  .overview-content {
    overflow-y: scroll;
  }
  .overview-left,
  .overview-right {
    font-size: 13px;
    transition: font-size 0.5s ease;
  }

  .overview-comment {
    font-size: 12px;
    transition: font-size 0.5s ease;
  }
}
</style>