<script setup lang ="ts">
import { ref, onMounted } from 'vue';
import { SongFeatureCategory, SongFeature } from '@/types/SongFeature';
import Dialog from 'primevue/dialog';
import Tabs from 'primevue/tabs';
import Chart from 'primevue/chart';
import { Chart as ChartJS, registerables } from 'chart.js';
import TabList from 'primevue/tablist';
import Tab from 'primevue/tab';
import TabPanels from 'primevue/tabpanels';
import TabPanel from 'primevue/tabpanel';

ChartJS.register(...registerables);

const props = defineProps<{
  flowerData: SongFeature[][],
  selectedFlowerIndex: number | null,
}>();

// TODO: Adjust scale for TEMPO.
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    customLegend: {
      drawLegend: false
      },
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

const chartData = (songFeatureCategory: SongFeatureCategory | null) => {
  // Adjust the color of the selected feature point.
  const pointColors = new Array(props.flowerData.length);
  pointColors.fill('grey');

  // Adjust the size of the selected feature point.
  const pointRadius = new Array(props.flowerData.length);
  pointRadius.fill(3);

  if (songFeatureCategory === null) {
    const datasets = Object.keys(SongFeatureCategory).filter((key) => isNaN(key)).map((categoryKey) => {
      const category = SongFeatureCategory[categoryKey];
      return {
        label: SongFeatureCategory[category],
        data: props.flowerData.flatMap(
          (flower) => flower.filter(
            (songFeature) => songFeature.category === category).map(
              (songFeature) => songFeature.value)
        ),
        fill: false,
        borderColor: colorPalettes[category],
        backgroundColor: colorPalettes[category],
        tension: 0.4
      };
    });

    return {
      labels: Array.from({ length: props.flowerData.length }, (_, i) => i + 1),
      datasets: datasets
    };
  } else {
    pointColors[props.selectedFlowerIndex] = colorPalettes[songFeatureCategory][0];
    pointRadius[props.selectedFlowerIndex] = 9;
    // generate for a specific feature
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
  }
};

const chartOptionsAllFeatures = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
        },
    customLegend: {
      drawLegend: true
      },
  },
  scales: {
    x: {
      type: 'linear',
      ticks: {
        padding: 10,
        autoSkip: false,
        stepSize: 1,
      },
      min: 1,
      max: (context) => context.chart.data.labels.length + 0.2,  // Add subtle space on the right
    },
    y: {
      min: 0,
      max: 1,
      ticks: {
        stepSize: 0.25
      }
    }
  }
};


// customize the legend
onMounted(() => {
  ChartJS.register({
    id: 'customLegend',
    afterDatasetDraw(chart, args) {

      if (!chart.options.plugins.customLegend || !chart.options.plugins.customLegend.drawLegend) {
        return;
      }

      const ctx = chart.ctx;
      const datasetMeta = args.meta;
      const dataset = chart.data.datasets[args.index];

      ctx.save();

      // Get the last data point in the dataset
      const lastDataPoint = datasetMeta.data[datasetMeta.data.length - 1];
      const { x, y } = lastDataPoint.tooltipPosition();  // Get x, y coordinates of the last data point

      const canvasWidth = chart.chartArea.right;

      let adjustedX = x + 10;
      let adjustedY = y - 10;

      // If the label is too close to the right edge, move it to the left
      if (adjustedX + 50 > canvasWidth) {
        adjustedX = x - 100;
      }

      // If the label is too close to the bottom edge, move it upwards
      if (adjustedY < 20) {
        adjustedY = y + 20;
      }

      // Iterate through previous datasets to avoid overlapping labels
      for (let i = 0; i < args.index; i++) {
        const previousDatasetMeta = chart.getDatasetMeta(i);
        const previousLastDataPoint = previousDatasetMeta.data[previousDatasetMeta.data.length - 1];
        const { x: prevX, y: prevY } = previousLastDataPoint.tooltipPosition();

        // Calculate distance between current and previous labels
        const distance = Math.sqrt((x - prevX) ** 2 + (y - prevY) ** 2);

        // If the labels are too close, adjust the current label position
        if (distance < 30) {
          adjustedY += 20;  // Increase offset more to prevent overlap
        }
      }

      // Draw the label at the adjusted position
      ctx.font = 'bold 14px Arial';
      ctx.fillStyle = dataset.borderColor;
      ctx.fillText(dataset.label, adjustedX, adjustedY);

      ctx.restore();
    }
  });
});
</script>

<template>
  <div>
    <Tabs :value="'ALL'" :unstyled="false">
      <TabList :unstyled="false" class="tabs">
          <Tab :value="'ALL'" :unstyled="false" class="all">All Features</Tab>
          <Tab :value="SongFeatureCategory.TEMPO" :unstyled="false" class="tempo">Tempo (BPM)</Tab>
          <Tab :value="SongFeatureCategory.ENERGY" :unstyled="false" class="energy">Energy</Tab>
          <Tab :value="SongFeatureCategory.VALENCE" :unstyled="false" class="valence">Valence</Tab>
          <Tab :value="SongFeatureCategory.DANCEABILITY" :unstyled="false" class="danceability">Danceability</Tab>
          <Tab :value="SongFeatureCategory.SPEECHINESS" :unstyled="false" class="speechiness">Speechiness</Tab>
      </TabList>
      <TabPanels>
          <TabPanel :value="'ALL'">
            <div class="chart">
              <Chart type="line" :data="chartData(null)" :options="chartOptionsAllFeatures" style="width: 100%; height: 100%"/>
            </div>
            <div class="text-container">
              <p class="m-0">
                  Comparison of all five song features together.
              </p>
            </div>
          </TabPanel>
          <TabPanel :value="SongFeatureCategory.TEMPO">
            <div class="chart">
              <Chart type="line" :data="chartData(SongFeatureCategory.TEMPO)" :options="chartOptions" style="width: 100%; height: 100%"/>
            </div>
            <div class="text-container">
              <p class="m-0">
                  The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.
              </p>
            </div>
          </TabPanel>
          <TabPanel :value="SongFeatureCategory.ENERGY">
              <div class="chart">
                <Chart type="line" :data="chartData(SongFeatureCategory.ENERGY)" :options="chartOptions" style="width: 100%; height: 100%"/>
              </div>
              <div class="text-container">
                <p class="m-0">
                  Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
                </p>
              </div>
          </TabPanel>
          <TabPanel :value="SongFeatureCategory.VALENCE">
              <div class="chart">
                <Chart type="line" :data="chartData(SongFeatureCategory.VALENCE)" :options="chartOptions" style="width: 100%; height: 100%"/>
              </div>
              <div class="text-container">
                <p class="m-0">
                  A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
                </p>
              </div>
          </TabPanel>
          <TabPanel :value="SongFeatureCategory.DANCEABILITY">
            <div class="chart">
                <Chart type="line" :data="chartData(SongFeatureCategory.DANCEABILITY)" :options="chartOptions" style="width: 100%; height: 100%"/>
              </div>
              <div class="text-container">
                <p class="m-0">
                  Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
                </p>
              </div>
          </TabPanel>
          <TabPanel :value="SongFeatureCategory.SPEECHINESS">
              <div class="chart">
                <Chart type="line" :data="chartData(SongFeatureCategory.SPEECHINESS)" :options="chartOptions" style="width: 100%; height: 100%"/>
              </div>
              <div class="text-container">
                <p class="m-0">
                  Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
              </p>
              </div>
          </TabPanel>
      </TabPanels>
    </Tabs>
  </div>
</template>

<style>
.chart {
  width: 100%;
  height: 25vh;
  margin-bottom: 10px;
}

.text-container {
  width: 85vw;
  text-align: left;
}

.text-container p {
  margin: 0;
}

.card {
  background: var(--card-bg);
  border: var(--card-border);
  padding: 2rem;
  border-radius: 10px;
  margin-bottom: 1rem;
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

.p-tab.all.p-tab-active {
  color: lightsteelblue;
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