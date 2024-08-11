<script setup lang="ts">
<<<<<<< HEAD
import {RouterView } from 'vue-router'
import {layoutService} from './services/layoutService'
import { onMounted, onUnmounted, nextTick } from 'vue'

onMounted(() => {
  layoutService.onResize();
  nextTick().then(() => {
      window.addEventListener('resize', () => layoutService.onResize());
  });
});

onUnmounted(() => {
  window.removeEventListener('resize', () => layoutService.onResize()); 
});
=======
import { RouterView } from 'vue-router'
>>>>>>> 6f4851c88abccd92dcd6fd90227113395ac7e547

</script>

<template>
  <RouterView />
</template>
<<<<<<< HEAD
=======

<style scoped>
</style>
>>>>>>> 6f4851c88abccd92dcd6fd90227113395ac7e547
