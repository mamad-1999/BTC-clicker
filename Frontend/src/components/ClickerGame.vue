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
    <UsernameModal :show="showUsernameModal" @close="onUsernameSubmit" />
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from "vue";
import axios from "axios";
import ClickCounter from "./ClickCounter.vue";
import ClickPower from "./ClickPower.vue";
import ClickButton from "./ClickButton.vue";
import ClickButtonUpgrades from "./ClickButtonUpgrades.vue";
import UsernameModal from "./UsernameModal.vue";
import upgradeFullList from "../upgrades.json";

const autoclickUpdateRate = 20;

export default {
  name: "ClickerGame",
  components: {
    ClickCounter,
    ClickPower,
    ClickButton,
    ClickButtonUpgrades,
    UsernameModal,
  },
  setup() {
    const clicks = ref(1000);
    const upgrades = reactive(Array(upgradeFullList.length).fill(0));
    const showUsernameModal = ref(true);
    const username = ref("");

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
        clicks.value +=
          upgrade.ratepersecond * upgrades[index] * rateMultiplier;
      });
    };

    const handleClick = () => {
      clicks.value++;
    };

    const handleUpgrades = (buttonId) => {
      upgrades[buttonId]++;
      clicks.value -= upgradeFullList[buttonId].minclicks;
    };

    const onUsernameSubmit = async (submittedUsername) => {
      username.value = submittedUsername;
      showUsernameModal.value = false;
    };

    const getLeaderboard = async () => {
      try {
        const response = await axios.get("/api/leaderboard");
        console.log("Leaderboard:", response.data);
        // Update your component state with this data
      } catch (error) {
        console.error("Error fetching leaderboard:", error);
      }
    };

    const sendScore = async () => {
      try {
        await axios.post("/send-score", {
          id: username.id,
          score: Math.floor(clicks.value),
        });
      } catch (error) {
        console.error("Error sending score:", error);
      }
    };

    onMounted(() => {
      setInterval(updateClicks, autoclickUpdateRate);
      setInterval(sendScore, 60000); // Send score every minute
    });

    return {
      clicks,
      clickDelta,
      state,
      upgradeFullList,
      showUsernameModal,
      handleClick,
      handleUpgrades,
      onUsernameSubmit,
    };
  },
};
</script>

<style scoped>
.clicker-window {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  position: relative;
}
</style>
