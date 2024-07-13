<!-- ClickerGame.vue -->
<template>
    <div class="clicker-window">
      <ClickCounter :clicks="clicks" :clickDelta="clickDelta" />
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
  import ClickButton from './ClickButton.vue';
  import ClickButtonUpgrades from './ClickButtonUpgrades.vue';
  import upgradeFullList from './upgrades.json';
  
  const autoclickUpdateRate = 20; // 20 ~ 50Hz
  
  export default {
    name: 'ClickerGame',
    components: {
      ClickCounter,
      ClickButton,
      ClickButtonUpgrades,
    },
    setup() {
      const clicks = ref(0);
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
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-image: linear-gradient(40deg, rgba(242, 169, 0, 1) 10%, rgba(211, 143, 0, 1) 20%, rgba(180, 117, 0, 1) 35%, rgba(150, 93, 0, 1) 45%, rgba(120, 69, 0, 1) 55%, rgba(91, 47, 0, 1) 65%, rgba(64, 26, 0, 1) 80%, rgba(39, 2, 0, 1) 90%, rgba(0, 0, 0, 1) 100%);
    gap: 20px;
    padding-top: 30px;
  }
  </style>