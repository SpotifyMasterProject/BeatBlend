<script setup lang="ts">
import { computed, defineProps } from 'vue';
const props = defineProps<{
  index: number;
  value: number;
  color: string;
  center: number;
  circleRadius: number;
}>();

const rotation = computed(() => (props.index * 360) / 5);

const petalPath = computed(() => {
  const petalLength = props.circleRadius + props.value * props.circleRadius;
  const baseWidth = props.circleRadius / 2;
  const offset = 0.2 * baseWidth;

  const controlPoint1X = props.center - baseWidth;
  const controlPoint1Y = props.center - petalLength / 2 - offset;
  const controlPoint2X = props.center + baseWidth;
  const controlPoint2Y = props.center - petalLength / 2 - offset;
  const endX = props.center;
  const endY = props.center - petalLength;

  return `
    M ${props.center} ${props.center}
    Q ${controlPoint1X} ${controlPoint1Y},
      ${endX} ${endY}
    Q ${controlPoint2X} ${controlPoint2Y},
      ${props.center} ${props.center}
  `;
});

function lightenColor(color: string, percent: number) {
  if (!color || typeof color !== 'string' || color.length !== 7 || color[0] !== '#') {
    console.error('Invalid color format:', color);
    return '#FFFFFF'; // Return a default color (white) in case of an error
  }
  const num = parseInt(color.slice(1), 16),
      amt = Math.round(2.55 * percent),
      R = (num >> 16) + amt,
      G = ((num >> 8) & 0x00ff) + amt,
      B = (num & 0x0000ff) + amt;
  return `#${(
      0x1000000 +
      (R < 255 ? (R < 1 ? 0 : R) : 255) * 0x10000 +
      (G < 255 ? (G < 1 ? 0 : G) : 255) * 0x100 +
      (B < 255 ? (B < 1 ? 0 : B) : 255)
  )
      .toString(16)
      .slice(1)}`;
}
</script>

<template>
  <g :transform="`rotate(${rotation}, ${center}, ${center})`">
    <path
        :d="petalPath"
        :fill="`url(#gradient${index})`"
    />
    <defs>
      <linearGradient :id="`gradient${index}`" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" :stop-color="lightenColor(color, 0.3)" />
        <stop offset="100%" :stop-color="color" />
      </linearGradient>
    </defs>
  </g>
</template>

<style scoped>
  path {
    transition: fill 0.3s ease;
  }
</style>