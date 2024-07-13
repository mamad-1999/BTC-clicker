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

  @media screen and (max-width: 400px) {
    #clicks{
    font-size: 65px;
  }
}
</style>

<!-- {{ clickDelta.toFixed(0) }} -->