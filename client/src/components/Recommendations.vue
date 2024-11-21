<script setup lang="ts">
import {ref, watch, onMounted, computed} from 'vue';
import Flower from "@/components/Flower.vue";
import { Song } from "@/types/Song";
import { getSongFeatures, getSongFeatureCategory } from "@/services/sessionService";

const props = defineProps<{
  recommendations: Song[],
  zoomLevel: number,
  lastFlowerPosition?: {
    x: number,
    y: number,
  }
}>();

const emit = defineEmits(['hover', 'leave']);

const flowerData = computed(() => {
  return props.recommendations.map((song) => {
    return {
      features: getSongFeatures(song),
      mostSignificantFeature: getSongFeatureCategory(song.mostSignificantFeature)
    };
  });
});

const localFlowerLinePositions = ref({});
const flowerLines = computed(() => {
  const lines = [];
  const currentFlower = props.lastFlowerPosition;
  if (!currentFlower) {
    return [];
  }
  for (let i = 0; i < flowerData.value.length; i++) {
    const nextFlower = globalFlowerLinePositions(localFlowerLinePositions.value[i], flowerPositions.value[i]);
    if (!currentFlower || !nextFlower) {
      return [];
    }
    lines.push(computeLineBetweenFlowers(currentFlower, nextFlower));
  }

  return lines;
});

const flowerPositions = computed(() => {
  if (!props.lastFlowerPosition) {
    return [];
  }
  const positions = [];
  const verticalDistance = -100;
  const horizontalDistance = 50;

  return props.recommendations.map((_, index) => {
    return {
      x: props.lastFlowerPosition.x + horizontalDistance,
      y: props.lastFlowerPosition.y - 40 + (index - 1) * verticalDistance,
    }
  })
});


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

</script>
<template>
    <Flower
      v-for="(flower, index) in flowerData"
      :features="flower.features"
      :mostSignificantFeature="flower.mostSignificantFeature"
      :circleRadius="30 * zoomLevel"
      :position="flowerPositions[index]"
      @significantFeaturePosition="(position) => storeFlowerLinePosition(position, index)"
      @hover="() => emit('hover', recommendations[index])"
      @leave="emit('leave')"
    />
    <path
      v-for="line in flowerLines"
      class="connecting-path"
      :d="line" stroke="white" fill="transparent"
    />
</template>
<style scoped>
.flower-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 100px;
}
.song-details-container {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  max-width: 200px;
  white-space: nowrap;
}
.song-details {
  overflow: hidden;
  text-overflow: ellipsis;
}
.recommendations-wrapper {
  display: flex;
  flex-direction: row;
}
.connecting-path {
  pointer-events: none;
}
</style>