<!-- ClickCounter.vue -->
<template>
    <p id="clicks">
      {{ Math.floor(clicks) }}
    </p>
</template>

<script>
export default {
  name: 'ClickCounter',
  props: {
    clicks: Number,
    clickDelta: Number,
  },
};
</script>

<style scoped>
  #clicks{
    color: aliceblue;
    font-size: 50px;
    font-weight: bold;
  }
</style>

<!-- Automatic Clicking Rate: {{ clickDelta.toFixed(0) }} clicks per second -->