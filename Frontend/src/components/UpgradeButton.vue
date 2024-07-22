<!-- UpgradeButton.vue -->
<template>
  <button
    :id="upgrade.id"
    class="update-button"
    type="button"
    @click="$emit('upgrade')"
    :disabled="isDisabled"
  >
    <span
      >{{ upgrade.label }} ({{ upgrade.ratepersecondlable }} PS) x
      {{ numUpgraded }}</span
    >
    <span class="cost">{{ upgrade.minclicklable }} BTC</span>
  </button>
</template>

<script>
import { computed } from "vue";

export default {
  name: "UpgradeButton",
  props: {
    upgrade: Object,
    state: Object,
  },
  emits: ["upgrade"],
  setup(props) {
    const numUpgraded = computed(() => props.state.upgrades[props.upgrade.id]);
    const isDisabled = computed(
      () => props.state.clicks < props.upgrade.minclicks
    );

    return {
      numUpgraded,
      isDisabled,
    };
  },
};
</script>

<style scoped>
.update-button {
  width: 100%;
  padding: 8px 8px;
  margin-right: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(
    60deg,
    rgba(222, 180, 13, 1) 0%,
    rgba(250, 212, 37, 1) 65%
  );
  font-weight: 600;
  color: #5b2f00;
  box-shadow: 2px 2px 10px #5b2f00;
  outline: none;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.5s ease;
}

.update-button:disabled {
  background: linear-gradient(
    60deg,
    rgb(163, 133, 10) 0%,
    rgb(170, 144, 25) 65%
  );
}

.cost {
  width: 80px;
  padding: 2px 4px;
  background-color: #ffffdf;
  font-weight: 600;
  color: rgb(105, 111, 117);
  border-radius: 10px;
}

.update-button:disabled .cost {
  background-color: #c7c7c7;
}

@media screen and (min-width: 768px) {
  .update-button {
    margin: 0 auto;
    padding: 10px 8px;
  }
}

@media screen and (max-width: 400px) {
  .update-button {
    padding: 12px 8px;
  }
}
</style>
