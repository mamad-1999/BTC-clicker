<!-- UpgradeButton.vue -->
<template>
    <button
      :id="upgrade.id"
      class="update-button"
      type="button"
      @click="$emit('upgrade')"
      :disabled="isDisabled"
    >
      <span>{{ upgrade.label }} ({{ upgrade.ratepersecond }} cps) x {{ numUpgraded }}</span>
      <span class="cost">{{ upgrade.minclicks }} BTC Cost</span>
    </button>
</template>

<script>
import { computed } from 'vue';

export default {
  name: 'UpgradeButton',
  props: {
    upgrade: Object,
    state: Object,
  },
  emits: ['upgrade'],
  setup(props) {
    const numUpgraded = computed(() => props.state.upgrades[props.upgrade.id]);
    const isDisabled = computed(() => props.state.clicks < props.upgrade.minclicks);

    return {
      numUpgraded,
      isDisabled,
    };
  },
};
</script>

<style scoped>
.update-button{
  background-color: #FFE050;
  outline: none;
  border: none;
  padding: 7px 8px;
  width: 100%;
  margin-right: 5px;
  display: flex;
  justify-content: space-between;
  border-radius: 10%;
  cursor: pointer;
}

.update-button:disabled{
  background-color: #FFFF89;
}

.cost{
  background-color: #FFFFDF;
  font-weight: 600;
  color: rgb(105, 111, 117);
}
</style>