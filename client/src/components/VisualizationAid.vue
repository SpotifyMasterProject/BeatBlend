<script setup lang="ts">
import { ref } from 'vue';
import Flower from './Flower.vue';
import Petal from './Petal.vue';

const showPopup = ref(true);

function closePopup(){
  showPopup.value = false;
}

</script>

<template>
  <div v-if="showPopup" class="popup-overlay">
    <div class="popup-content">
      <div class="popup-header">
        <h1>How to read the graph</h1>
        <button class="close-button" @click="$emit('close-popup')">✕</button>
      </div>
      <div class="popup-body">
        <div class="popup-column column-1">
          <div class ="flower-ruler-container">
            <svg width="160" height="160">
              <circle cx="80" cy="80" r="40" fill="none" stroke="#FFFFFF" stroke-width="2"/>
              <Petal
                  :index="0"
                  :value="1"
                  :center="80"
                  :circleRadius="40"
                  fill="none"
              />
              <Petal
                  :index="0"
                  :value="0.5"
                  :center="80"
                  :circleRadius="40"
                  fill="none"
              />
            </svg>
            <!-- Ruler -->
            <div class="ruler">
              <div class="ruler-line"></div>
              <div class="horizontal-line" style="top: 0%;"></div>
              <div class="horizontal-line" style="top: 25%;"></div>
              <div class="horizontal-line" style="top: 50%;"></div>
              <div class="ruler-label" style="top: 0%;">1</div>
              <div class="ruler-label" style="top: 25%;">0.5</div>
              <div class="ruler-label" style="top: 50%;">0</div>
            </div>
          </div>
          <!-- Left Column: Circle and one Petal -->
          <div class="petal-explanation">
            <p>Each petal represents a feature. The length and width are determined by the feature's value, ranging from 0 (center) to 1 (edge).</p>
          </div>
        </div>
        <div class="vertical-line"></div>
        <div class="popup-column column-2">
          <!-- Right Column: Flower and Audio Features Below -->
          <div class="flower-container">
            <Flower :features="[
              { value: 0.5, color: '#0F3740' },
              { value: 0.5, color: '#283618' },
              { value: 0.5, color: '#F38E36' },
              { value: 0.5, color: '#A65FDD' },
              { value: 0.5, color: '#EEE8C4' }
            ]"/>
          </div>
          <div class="petal-descriptions-horizontal">
            <div class="petal-description">
              <div class="petal-color" style="background-color: #0F3740;"></div>
              <p>Energy</p>
            </div>
            <div class="petal-description">
              <div class="petal-color" style="background-color: #283618;"></div>
              <p>Danceability</p>
            </div>
            <div class="petal-description">
              <div class="petal-color" style="background-color: #F38E36;"></div>
              <p>Speechiness</p>
            </div>
            <div class="petal-description">
              <div class="petal-color" style="background-color: #A65FDD;"></div>
              <p>Valence</p>
            </div>
            <div class="petal-description">
              <div class="petal-color" style="background-color: #EEE8C4;"></div>
              <p>Tempo</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

.popup-content {
  background-color: var(--backcore-color1);
  border-radius: 8px;
  padding: 20px;
  width: 60%;
  max-width: 800px;
  color: white;
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}

.popup-header h1 {
  margin: 20px;
  font-size: 24px;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  color: white;
  cursor: pointer;
}

.popup-body {
  display: flex;
  flex-direction: row;
  gap: 20px;
  aligns-items: center;
}

.popup-column {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.column-1 {
  flex: 1;
  display: flex;
  justify-content: center;
}

.column-2 {
  flex: 3;
  padding-left: 20px;
  padding-right: 10px;
  flex-direction: column;
  align-items: center;
}

.vertical-line {
  margin-left: 30px;
  width: 1px;
  background-color: white;
  height: auto; /* Make sure it stretches to the full height of the container */
}

.flower-ruler-container {
  position: relative;
  display: flex;
  align-items: center;
}

.ruler {
  position: absolute;
  top: 0;
  right: 0px;
  height: 160px; /* Match SVG height */
}

.ruler-line {
  width: 1px;
  height: 80px;
  background-color: #FFFFFF;
  position: absolute;
  top: 0;
  left: -10px;
}

.horizontal-line {
  width: 20px;
  height: 1px;
  background-color: #FFFFFF;
  position: absolute;
  left: -10px;
  transform: translateX(-50%);
}

.ruler-label {
  font-size: 12px;
  color: #FFFFFF;
  text-align: center;
  position: absolute;
  transform: translateY(-50%);
  left: 10px;
}

.petal-explanation {
  margin-left: 20px;
  text-align: center;
  font-size: 12px;
}

.flower-container {
  margin-bottom: 20px;

}

.petal-descriptions-horizontal {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  gap: 10px;
  width: 100%;
  text-align: center;
  flex-wrap: wrap;
}

.petal-description {
  flex: 1 1 18%; /* Allow each item to grow and shrink equally, with a base of 20% */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 12px;
}

.petal-color {
  width: 20px;
  height: 20px;
  border-radius: 50%;
}
</style>