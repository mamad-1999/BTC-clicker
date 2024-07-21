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
import { computed } from "vue";
import UpgradeButton from "./UpgradeButton.vue";

export default {
  name: "ClickButtonUpgrades",
  components: {
    UpgradeButton,
  },
  props: {
    upgradeFullList: Array,
    state: Object,
  },
  emits: ["upgrade"],
  setup(props) {
    const visibleUpgrades = computed(() => {
      return props.upgradeFullList.filter((upgrade, index) => {
        return (
          props.state.upgrades[index] > 0 ||
          props.state.clicks >= upgrade.minclicks
        );
      });
    });

    return {
      visibleUpgrades,
    };
  },
};
</script>

<style scoped>
.list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 90%;
  height: 250px;
  overflow-y: scroll;
  padding: 20px 10px;
}

::-webkit-scrollbar {
  width: 2px;
}
::-webkit-scrollbar-thumb {
  background-color: #f5d547;
  border-radius: 30px;
}

@media screen and (min-width: 768px) {
  .list {
    width: 50%;
  }
}
</style>
