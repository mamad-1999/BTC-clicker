<!-- ClickCounter.vue -->
<template>
  <p id="clicks">
    {{ formatLargeNumber(clicks) }}
  </p>
</template>

<script>
export default {
  name: 'ClickCounter',
  props: {
    clicks: Number,
    clickDelta: Number,
  },
  methods: {
    formatLargeNumber(num) {
      if (num < 1000000) {
        return Math.floor(num).toLocaleString();
      } else {
        const millions = (num / 1000000).toFixed();
        return parseFloat(millions).toString() + 'M';
      }
    }
  }
};
</script>

<style scoped>
#clicks {
  color: aliceblue;
  font-size: 50px;
  font-weight: bold;
}

@media screen and (max-width: 400px) {
  #clicks {
    font-size: 65px;
  }
}
</style>