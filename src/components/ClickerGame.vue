<!-- ClickerGame.vue -->
<template>
    <div class="clicker-window">
      <ClickPower :clickDelta="clickDelta" />
      <ClickCounter :clicks="clicks" />
      <ClickButton @click="handleClick" />
      <ClickButtonUpgrades
        :upgradeFullList="upgradeFullList"
        :state="state"
        @upgrade="handleUpgrades"
      />
    </div>
  </template>
  
  <script>
  import { ref, reactive, computed, onMounted } from 'vue';
  import ClickCounter from './ClickCounter.vue';
  import ClickPower from './clickPower.vue'
  import ClickButton from './ClickButton.vue';
  import ClickButtonUpgrades from './ClickButtonUpgrades.vue';
  import upgradeFullList from '../upgrades.json';
  
  const autoclickUpdateRate = 20;
  
  export default {
    name: 'ClickerGame',
    components: {
      ClickCounter,
      ClickPower,
      ClickButton,
      ClickButtonUpgrades,
    },
    setup() {
      const clicks = ref(1000);
      const upgrades = reactive(Array(upgradeFullList.length).fill(0));
  
      const state = reactive({
        clicks,
        upgrades,
      });
  
      const clickDelta = computed(() => {
        return upgradeFullList.reduce((total, upgrade, index) => {
          return total + upgrade.ratepersecond * upgrades[index];
        }, 0);
      });
  
      const updateClicks = () => {
        const rateMultiplier = autoclickUpdateRate / 1000;
        upgradeFullList.forEach((upgrade, index) => {
          clicks.value += upgrade.ratepersecond * upgrades[index] * rateMultiplier;
        });
      };
  
      const handleClick = () => {
        clicks.value++;
      };
  
      const handleUpgrades = (buttonId) => {
        upgrades[buttonId]++;
        clicks.value -= upgradeFullList[buttonId].minclicks;
      };
  
      onMounted(() => {
        setInterval(updateClicks, autoclickUpdateRate);
      });
  
      return {
        clicks,
        clickDelta,
        state,
        upgradeFullList,
        handleClick,
        handleUpgrades,
      };
    },
  };
  </script>
  
  <style scoped>
  .clicker-window{
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    position: relative;
  }
  </style>