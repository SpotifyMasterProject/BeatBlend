<script setup lang ="ts">
import {ref} from 'vue';
import { SongFeatureCategory, SongFeature } from '@/types/SongFeature';
import Dialog from 'primevue/dialog';
import Tabs from 'primevue/tabs';
import Chart from 'primevue/chart';
import TabList from 'primevue/tablist';
import Tab from 'primevue/tab';
import TabPanels from 'primevue/tabpanels';
import TabPanel from 'primevue/tabpanel';

const props = defineProps<{
  flowerData: SongFeature[][],
  currentSelectedFeature?: {index: number, featureCategory: SongFeatureCategory};
}>();

const visible = defineModel();

// TODO: Adjust scale for TEMPO.
const chartOptions = {
  aspectRatio: 4.0,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      min: 0,
      max: 1,
      ticks: {
        stepSize: 0.25
      }
    }
  }
};

const colorPalettes = {
  [SongFeatureCategory.DANCEABILITY]: ['#25606C'],
  [SongFeatureCategory.ENERGY]: ['#4D6730'],
  [SongFeatureCategory.SPEECHINESS]: ['#DED9BA'],
  [SongFeatureCategory.TEMPO]: ['#BC6C26'],
  [SongFeatureCategory.VALENCE]: ['#A65FDD'],
};

const chartData = (songFeatureCategory: SongFeatureCategory) => {
  // Adjust the color of the selected feature point.
  const pointColors = new Array(props.flowerData.length);
  pointColors.fill('grey');
  pointColors[props.currentSelectedFeature.index] = colorPalettes[songFeatureCategory][0];

  // Adjust the size of the selected feature point.
  const pointRadius = new Array(props.flowerData.length);
  pointRadius.fill(3);
  pointRadius[props.currentSelectedFeature.index] = 7;

  // Create a line chart showing all the features.
  return {
    labels: Array.from({length: props.flowerData.length}, (_, i) => i + 1),
    datasets: [
        {
          label: "Data",
            data: props.flowerData.flatMap(
              (flower) => flower.filter(
                (songFeature) => songFeature.category === songFeatureCategory).map(
                  (songFeature) => songFeature.value)
                ),
            fill: false,
            borderColor: 'grey',
            tension: 0.4,
            pointBackgroundColor: pointColors,
            pointRadius: pointRadius
        }
    ]
  };
};
</script>

<template>
  <Dialog
      v-model:visible="visible"
      modal
      dismissableMask
      :style="{
        backgroundColor: 'var(--backcore-color3)',
        width: '700px',
        padding: '10px',
      }"
      :unstyled="false">
    <Tabs :value="currentSelectedFeature.featureCategory ?? SongFeatureCategory.TEMPO" :unstyled="false">
      <TabList :unstyled="false" class="tabs">
          <Tab :value="SongFeatureCategory.TEMPO" :unstyled="false" class="tempo">Tempo (BPM)</Tab>
          <Tab :value="SongFeatureCategory.ENERGY" :unstyled="false" class="energy">Energy</Tab>
          <Tab :value="SongFeatureCategory.VALENCE" :unstyled="false" class="valence">Valence</Tab>
          <Tab :value="SongFeatureCategory.DANCEABILITY" :unstyled="false" class="danceability">Danceability</Tab>
          <Tab :value="SongFeatureCategory.SPEECHINESS" :unstyled="false" class="speechiness">Speechiness</Tab>
      </TabList>
      <TabPanels>
          <TabPanel :value="SongFeatureCategory.TEMPO">
              <Chart type="line" :data="chartData(SongFeatureCategory.TEMPO)" :options="chartOptions" />
              <p class="m-0">
                  The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.
              </p>
          </TabPanel>
          <TabPanel :value="SongFeatureCategory.ENERGY">
              <Chart type="line" :data="chartData(SongFeatureCategory.ENERGY)" :options="chartOptions" />
              <p class="m-0">
                  Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
              </p>
          </TabPanel>
          <TabPanel :value="SongFeatureCategory.VALENCE">
              <Chart type="line" :data="chartData(SongFeatureCategory.VALENCE)" :options="chartOptions" />
              <p class="m-0">
                  A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
              </p>
          </TabPanel>
          <TabPanel :value="SongFeatureCategory.DANCEABILITY">
              <Chart type="line" :data="chartData(SongFeatureCategory.DANCEABILITY)" :options="chartOptions" />
              <p class="m-0">
                  Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
              </p>
          </TabPanel>
          <TabPanel :value="SongFeatureCategory.SPEECHINESS">
              <Chart type="line" :data="chartData(SongFeatureCategory.SPEECHINESS)" :options="chartOptions" />
              <p class="m-0">
                  Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
              </p>
          </TabPanel>
      </TabPanels>
    </Tabs>
  </Dialog>
</template>

<style>
.card {
  background: var(--card-bg);
  border: var(--card-border);
  padding: 2rem;
  border-radius: 10px;
  margin-bottom: 1rem;
}

.song-feature-dialog {
  width: 200px;
  height: 200px;
}

/* Specify class 2 times to override default values set by primevue theme. */
.tabs.tabs {
  justify-content: center;
}

/* Specify class 2 times to override default values set by primevue theme. */
.p-tablist-content.p-tablist-content {
  flex-grow: 0;
}

/* Specify class 2 times to override default values set by primevue theme. */
.p-tablist-tab-list.p-tablist-tab-list {
  border-width: 0px;
}

/* Specify class 2 times to override default values set by primevue theme. */
.p-tab.p-tab {
  border-width: 0px;
  padding: 10px;
  font-weight: bold;
}

/* Specify class 2 times to override default values set by primevue theme. */
.p-tab.tempo.p-tab-active {
  color: var(--tempo-color);
}

.p-tab.valence.p-tab-active {
  color: var(--valence-color);
}

.p-tab.speechiness.p-tab-active {
  color: var(--speechiness-color);
}

.p-tab.danceability.p-tab-active {
  color: var(--danceability-color);
}

.p-tab.energy.p-tab-active {
  color: var(--energy-color);
}

/* Specify class 2 times to override default values set by primevue theme. */
.p-dialog-header.p-dialog-header {
  justify-content: end;
}

/* Specify class 2 times to override default values set by primevue theme. */
.p-overlay-mask.p-overlay-mask {
  background-color: rgba(0, 0, 0, 0.7);
}
</style>