<!-- ClickButtonUpgrades.vue -->
<template>
    <ul class="list">
      <li v-for="upgrade in visibleUpgrades" :key="upgrade.id">
        <UpgradeButton
          :upgrade="upgrade"
          :state="state"
          @upgrade="$emit('upgrade', upgrade.id)"
        />
      </li>
    </ul>
</template>

<script>
import { computed } from 'vue';
import UpgradeButton from './UpgradeButton.vue';

export default {
  name: 'ClickButtonUpgrades',
  components: {
    UpgradeButton,
  },
  props: {
    upgradeFullList: Array,
    state: Object,
  },
  emits: ['upgrade'],
  setup(props) {
    const visibleUpgrades = computed(() => {
      return props.upgradeFullList.filter((upgrade, index) => {
        return props.state.upgrades[index] > 0 || props.state.clicks >= upgrade.minclicks;
      });
    });

    return {
      visibleUpgrades,
    };
  },
};
</script>

<style scoped>
.list{
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 90%;
  height: 100%;
}
</style>