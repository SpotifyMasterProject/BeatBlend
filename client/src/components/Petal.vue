<script setup lang="ts">
import { computed, defineProps } from 'vue';

const props = defineProps<{
  index: number;
  value: number;
  center: number;
  circleRadius: number;
}>();

const rotation = computed(() => (props.index * 360) / 5);

const colorPalettes = {
  blue: ['#0F3740', '#144550', '#194E59', '#1D5864', '#25606C'],
  green: ['#283618', '#31431E', '#3C5125', '#4D6730', '#597738'],
  beige: ['#DED9BA', '#EEE8C4', '#F4EEC8', '#F8F2CD', '#FEFAE1'],
  orange: ['#BC6C26', '#CD762A', '#E4832E', '#F38E36', '#F99945'],
  pink: ['#A65FDD', '#B36DEA', '#BB7DEC', '#C093E4', '#CCA9E9'],
} as const; // This makes the object keys and values readonly

type ColorPaletteKey = keyof typeof colorPalettes;

const getColorPaletteForIndex = (index: number) => {
  const paletteKeys = Object.keys(colorPalettes) as ColorPaletteKey[];
  const selectedPaletteKey = paletteKeys[index % paletteKeys.length];
  return colorPalettes[selectedPaletteKey];
};

const calculateEllipseArea = (width: number, height: number) => {
  return Math.PI * (width / 2) * (height / 2);
};

const generatePetalPath = (totalLength: number, totalWidth: number) => {
  const pathData: string[] = [];
  const sections = 5;
  const totalArea = calculateEllipseArea(totalWidth, totalLength);

  // Calculate the area for each section (linear distribution)
  const sectionAreas = Array.from({ length: sections }, (_, i) => (totalArea / sections) * (i + 1));

  // Generate paths for each section
  sectionAreas.forEach((area, i) => {
    const normalizedValue = Math.sqrt((i + 1) / sections);
    const sectionHeight = totalLength * normalizedValue;
    const sectionWidth = Math.sqrt((area / Math.PI) * 5); // Calculate width based on area and height

    const controlOffset = sectionWidth / 2;
    const controlPoint1X = props.center - controlOffset;
    const controlPoint1Y = props.center - sectionHeight / 2;
    const controlPoint2X = props.center + controlOffset;
    const controlPoint2Y = props.center - sectionHeight / 2;
    const endX = props.center;
    const endY = props.center - sectionHeight;

    const path = `
      M ${props.center} ${props.center}
      Q ${controlPoint1X} ${controlPoint1Y},
        ${endX} ${endY}
      Q ${controlPoint2X} ${controlPoint2Y},
        ${props.center} ${props.center}
    `;
    pathData.push(path);
  });

  return pathData;
};

const petalPaths = computed(() => {
  const baseRadius = props.circleRadius; // Base radius is 40px
  const petalLength = baseRadius * props.value * 2; // Petal length based on value
  const maxMidWidth = petalLength / 2; // Make the middle the broadest part

  return generatePetalPath(petalLength, maxMidWidth);
});

const petalColors = computed(() => getColorPaletteForIndex(props.index));


</script>

<template>
  <g :transform="`rotate(${rotation}, ${center}, ${center})`">
    <path
        v-for="(path, i) in petalPaths"
        :key="i"
        :d="path"
        :fill="petalColors[i]"
        stroke="rgba(255, 255, 255, 0.3)"
        stroke-width="0.5"
    />
  </g>
</template>

<style scoped>
path {
  transition: fill 0.3s ease;
}
</style>