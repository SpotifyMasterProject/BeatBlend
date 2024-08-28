<script setup lang ="ts">
import { computed, defineProps} from 'vue';
import Petal from './Petal.vue';

const props = defineProps<{
  features: { value: number; color: string }[];
  size?: number;
  circleRadius?: number;
}>();
const size = props.size ?? 80;
const circleRadius = props.circleRadius ?? 40;

const maxPetalLength = computed(() => circleRadius + Math.max(...props.features.map(f => f.value * circleRadius)));
const center = computed(() => size / 2);
const rotation = computed(() => {
  const maxFeatureIndex = props.features.reduce(
      (maxIndex, feature, index, features) =>
          feature.value > features[maxIndex].value ? index : maxIndex,
      0
  );
  return (maxFeatureIndex * 360) / props.features.length;
});
</script>

<template>
  <svg :width="maxPetalLength * 2" :height="maxPetalLength * 2" :viewBox="`0 0 ${maxPetalLength * 2} ${maxPetalLength * 2}`" :style="{ transform: `rotate(${rotation}deg)` }">
    <circle :cx="maxPetalLength" :cy="maxPetalLength" :r="circleRadius" fill="none" stroke="#CCCCCC" stroke-width="1" />
    <Petal
        v-for="(feature, index) in features"
        :key="index"
        :index="index"
        :value="feature.value"
        :color="feature.color"
        :center="maxPetalLength"
        :circleRadius="circleRadius"
    />
  </svg>
</template>


<style scoped>
  svg {
    display: block;
    margin: auto;
  }
</style>