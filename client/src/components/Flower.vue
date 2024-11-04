<script setup lang ="ts">
import { computed, defineProps, useTemplateRef, onMounted } from 'vue';
import Petal from './Petal.vue';
import { SongFeature, SongFeatureCategory } from '@/types/SongFeature';

const props = defineProps<{
  features: SongFeature[];
  position?: {x: number, y: number};
  size?: number;
  circleRadius?: number;
  mostSignificantFeature?: SongFeatureCategory
}>();

const emit = defineEmits(['onPetalClick', 'significantFeaturePosition', 'hover', 'leave']);


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

const flower = useTemplateRef('flower');

const onPetalEndPositionComputed = (position, songFeatureCategory) => {
  if (songFeatureCategory === props.mostSignificantFeature) {
    emit('significantFeaturePosition', position);
  }
};

onMounted(() => {
  if (props.mostSignificantFeature === null) {
    emit('significantFeaturePosition', {x: maxPetalLength.value, y: maxPetalLength.value});
  }
  console.log(props.position);
});

</script>

<template>
  <svg
    ref="flower"
    :x="position?.x"
    :y="position?.y"
    :width="maxPetalLength * 2"
    :height="maxPetalLength * 2"
    @mouseenter="() => emit('hover')"
    @mouseleave="() => emit('leave')">
      <circle :cx="maxPetalLength" :cy="maxPetalLength" :r="circleRadius" fill="none" stroke="#CCCCCC" stroke-width="1" />
      <Petal
          class="petal"
          v-for="(feature, index) in features"
          :key="index"
          :index="index"
          :feature="feature"
          :center="maxPetalLength"
          :circleRadius="circleRadius"
          :rotation="rotation"
          @click="() => emit('onPetalClick', feature.category)"
          @emitEndPosition="(position) => onPetalEndPositionComputed(position, feature.category)"
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