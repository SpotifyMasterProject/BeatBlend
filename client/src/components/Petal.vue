<script>
export default {
  name: 'Petal',
  props: {
    index: Number,
    value: Number,
    color: String,
    center: Number,
    circleRadius: Number,
  },
  computed: {
    rotation() {
      return (this.index * 360) / 5;
    },
    petalPath() {
      const petalLength = this.circleRadius + this.value * this.circleRadius;
      const baseWidth = this.circleRadius / 2;
      const offset = 0.2 * baseWidth;

      const controlPoint1X = this.center - baseWidth;
      const controlPoint1Y = this.center - petalLength / 2 - offset;
      const controlPoint2X = this.center + baseWidth;
      const controlPoint2Y = this.center - petalLength / 2 - offset;
      const endX = this.center;
      const endY = this.center - petalLength;

      return `
        M ${this.center} ${this.center}
        Q ${controlPoint1X} ${controlPoint1Y},
          ${endX} ${endY}
        Q ${controlPoint2X} ${controlPoint2Y},
          ${this.center} ${this.center}
      `;
    },
  },
  methods: {
    lightenColor(color, percent) {
      const num = parseInt(color.slice(1), 16),
          amt = Math.round(2.55 * percent),
          R = (num >> 16) + amt,
          G = (num >> 8 & 0x00FF) + amt,
          B = (num & 0x0000FF) + amt;
      return `#${(0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 + (G < 255 ? G < 1 ? 0 : G : 255) * 0x100 + (B < 255 ? B < 1 ? 0 : B : 255)).toString(16).slice(1)}`;
    },
  },
};
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