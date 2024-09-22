<script setup lang ="ts">
import { computed} from 'vue';
import Petal from './Petal.vue';
import { SongFeature } from '@/types/SongFeature';

const props = defineProps<{
  features: SongFeature[];
  circleRadius?: number;
}>();

const emit = defineEmits(['onPetalClick']);

const circleRadius = props.circleRadius ?? 40;

const maxPetalLength = computed(() => circleRadius + Math.max(...props.features.map(f => f.value * circleRadius)));
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
        class="petal"
        v-for="(feature, index) in features"
        :key="index"
        :index="index"
        :feature="feature"
        :center="maxPetalLength"
        :circleRadius="circleRadius"
        @click="() => emit('onPetalClick', feature.category)"
    />
  </svg>
</template>


<style scoped>
svg {
  display: block;
  margin: auto;
}

.petal {
  cursor: pointer;
}
</style>