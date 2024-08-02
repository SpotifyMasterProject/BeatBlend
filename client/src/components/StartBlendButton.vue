<script>
export default {
  name: "StartBlendButton",
  data() {
    return {
      hover:false
    }
  }
}

</script>

<template>
  <button class="start-blend" @mouseover="hover = true" @mouseleave="hover=false">
  Start Blend
  </button>

</template>

<style scoped>
.start-blend {
  background-color: #272525;
  color: white;
  border: none;
  border-radius: 50%;
  width: 200px;
  height: 200px;
  font-size: 1.5em;
  cursor: pointer;
  outline: none;
  transition: background-color 0.3s;
}
.start-blend:hover {
  background-color: #363636;
}
</style>