<template>
  <div class="clicker-window">
    <div class="leaderboard-icon" @click="showLeaderboardModal">
      <svg
        fill="aliceblue"
        width="35px"
        height="35px"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M22,7H16.333V4a1,1,0,0,0-1-1H8.667a1,1,0,0,0-1,1v7H2a1,1,0,0,0-1,1v8a1,1,0,0,0,1,1H22a1,1,0,0,0,1-1V8A1,1,0,0,0,22,7ZM7.667,19H3V13H7.667Zm6.666,0H9.667V5h4.666ZM21,19H16.333V9H21Z"
        />
      </svg>
    </div>
    <ClickPower :clickDelta="clickDelta" />
    <ClickCounter :clicks="clicks" />
    <ClickButton @click="handleClick" />
    <ClickButtonUpgrades
      :upgradeFullList="upgradeFullList"
      :state="state"
      @upgrade="handleUpgrades"
    />
    <UsernameModal :show="showUsernameModal" @close="onUsernameSubmit" />
    <LeaderboardModal
      :show="showLeaderboard"
      :leaderboard="leaderboard"
      @close="showLeaderboard = false"
    />
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch, onUnmounted } from "vue";
import axios from "axios";
import { debounce } from "lodash";
import ClickCounter from "./ClickCounter.vue";
import ClickPower from "./ClickPower.vue";
import ClickButton from "./ClickButton.vue";
import ClickButtonUpgrades from "./ClickButtonUpgrades.vue";
import UsernameModal from "./UsernameModal.vue";
import LeaderboardModal from "./LeaderboardModal.vue";
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
    LeaderboardModal,
  },
  setup() {
    const clicks = ref(1000000);
    const upgrades = reactive(Array(upgradeFullList.length).fill(0));
    const showUsernameModal = ref(true);
    const showLeaderboard = ref(false);
    const userData = ref({});
    const lastSentScore = ref(0);
    const leaderboard = ref([]);

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
      userData.username = submittedUsername.username;
      userData.id = submittedUsername.id;

      console.log(userData);

      showUsernameModal.value = false;
    };

    const showLeaderboardModal = () => {
      showLeaderboard.value = true;
      getLeaderboard();
    };

    const getLeaderboard = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000//get-users");

        // Check if the response is valid JSON
        if (response.headers["content-type"].includes("application/json")) {
          leaderboard.value = response.data.slice(0, 50); // Get top 10 players
        } else {
          console.error(
            "Invalid response format. Expected JSON, got:",
            response.headers["content-type"]
          );
          leaderboard.value = []; // Set to empty array if response is not JSON
        }
      } catch (error) {
        console.error("Error fetching leaderboard:", error);
        leaderboard.value = []; // Set to empty array on error
      }
    };

    const sendScore = async () => {
      try {
        await axios.post("http://127.0.0.1:5000/send-score", {
          id: userData.id,
          score: Math.floor(clickDelta.value),
        });
        getLeaderboard(); // Update leaderboard after sending score
      } catch (error) {
        console.error("Error sending score:", error);
      }
    };

    const debouncedSendScore = debounce(sendScore, 3000);

    const sendScoreIfSignificantChange = () => {
      const currentScore = Math.floor(clickDelta.value);
      if (
        currentScore - lastSentScore.value > 10 ||
        currentScore < lastSentScore.value
      ) {
        debouncedSendScore();
        lastSentScore.value = currentScore;
      }
    };

    watch(clickDelta, (newValue, oldValue) => {
      if (newValue !== oldValue) {
        sendScoreIfSignificantChange();
      }
    });

    onMounted(() => {
      setInterval(updateClicks, autoclickUpdateRate);
      getLeaderboard(); // Initial leaderboard fetch
    });

    onUnmounted(() => {
      sendScore(); // Ensure final score is sent
    });

    return {
      clicks,
      clickDelta,
      state,
      upgradeFullList,
      showUsernameModal,
      showLeaderboard,
      leaderboard,
      handleClick,
      handleUpgrades,
      onUsernameSubmit,
      showLeaderboardModal,
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
.leaderboard-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
  /* Add more styles for your icon */
}

.leaderboard-icon img {
  width: 50px;
  height: 50px;
}
</style>
