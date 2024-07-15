<!-- UpgradeButton.vue -->
<template>
    <button
      :id="upgrade.id"
      class="update-button"
      type="button"
      @click="$emit('upgrade')"
      :disabled="isDisabled"
    >
      <span>{{ upgrade.label }} ({{ upgrade.ratepersecond }} PS) x {{ numUpgraded }}</span>
      <span class="cost">{{ upgrade.minclicklable }} BTC</span>
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
  background-color: #f5d547;
  outline: none;
  border: none;
  padding: 8px 8px;
  width: 100%;
  margin-right: 5px;
  display: flex;
  justify-content: space-between;
  border-radius: 15%;
  cursor: pointer;
  box-shadow: 2px 2px 10px #5B2F00;
  color: #5B2F00;
  font-weight: 600;
}

.update-button:disabled{
  background-color: #be9341;
}


.cost{
  width: 90px;
  background-color: #FFFFDF;
  font-weight: 600;
  color: rgb(105, 111, 117);
  border-radius: 10px;
  padding: 2px 4px;
}

.update-button:disabled .cost{
  background-color: #c7c7c7;
}

@media screen and (min-width: 768px) {
  .update-button{
    width: 50%;
    margin: 0 auto;
    padding: 10px 8px;
  }
}

@media screen and (max-width: 400px) {
  .update-button{
    padding: 12px 8px;
  }
}
</style>