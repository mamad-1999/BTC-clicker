<!-- ClickCounter.vue -->
<template>
  <p id="clicks">
    {{ formatLargeNumber(clicks) }}
  </p>
</template>

<script>
export default {
  name: "ClickCounter",
  props: {
    clicks: Number,
    clickDelta: Number,
  },
  methods: {
    formatLargeNumber(num) {
      if (num < 1_000_000) {
        return Math.floor(num).toLocaleString();
      } else if (num < 1_000_000_000 && num >= 1_000_000) {
        const millions = (num / 1_000_000).toFixed(2);
        return millions.toString() + "M";
      } else {
        const billions = (num / 1_000_000_000).toFixed(3);
        return billions.toString() + "B";
      }
    },
  },
};
</script>

<style scoped>
#clicks {
  margin-top: 45px;
  font-size: 50px;
  font-weight: bold;
  color: aliceblue;
}

@media screen and (max-width: 400px) {
  #clicks {
    font-size: 60px;
  }
}
</style>
