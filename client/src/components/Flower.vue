<script>
import Petal from './Petal.vue';

export default {
  name: 'Flower',
  components: { Petal },
  props: {
    features: {
      type: Array,
      required: true,
      default: () => [
        { value: 0.4, color: '#144550' },
        { value: 0.6, color: '#31431E' },
        { value: 0.5, color: '#EEE8C4' },
        { value: 0.7, color: '#E4832E' },
        { value: 0.3, color: '#BB7DEC' },
      ],
    },
    size: {
      type: Number,
      default: 200,
    },
    circleRadius: {
      type: Number,
      default: 50,
    },
  },
  computed: {
    center() {
      return this.size / 2;
    },
    rotation() {
      const maxFeatureIndex = this.features.reduce((maxIndex, feature, index, features) =>
          feature.value > features[maxIndex].value ? index : maxIndex, 0
      );
      return (maxFeatureIndex * 360) / this.features.length;
    },
  },
};
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