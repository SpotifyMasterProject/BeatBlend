<script setup>
import { computed, defineProps} from 'vue';
import Petal from './Petal.vue';

const props = defineProps({
  features: {
    type: Array,
    required: true,
    validator: (value) => Array.isArray(value) && value.length === 5,
  },
  size: {
    type: Number,
    default: 100,
  },
  circleRadius: {
    type: Number,
    default: 50,
  },
});

const center = computed(() => props.size / 2);
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
  <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`" :style="{ transform: `rotate(${rotation}deg)` }">
    <circle :cx="center" :cy="center" :r="circleRadius" fill="none" stroke="#CCCCCC" stroke-width="1" />
    <Petal
        v-for="(feature, index) in features"
        :key="index"
        :index="index"
        :value="feature.value"
        :color="feature.color"
        :center="center"
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