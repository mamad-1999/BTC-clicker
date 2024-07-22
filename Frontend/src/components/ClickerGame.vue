<template>
  <div class="clicker-window">
    <div class="leaderboard-icon" @click="showLeaderboardModal">
      <button>show</button>
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
    const clicks = ref(1000);
    const upgrades = reactive(Array(upgradeFullList.length).fill(0));
    const showUsernameModal = ref(true);
    const showLeaderboard = ref(false);
    const username = ref("");
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
      console.log(submittedUsername);
      username.value = submittedUsername;
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
          leaderboard.value = response.data.slice(0, 10); // Get top 10 players
          console.log("Leaderboard:", leaderboard.value);
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
          id: username.value,
          score: Math.floor(clickDelta.value),
        });
        console.log("Score sent successfully");
        getLeaderboard(); // Update leaderboard after sending score
      } catch (error) {
        console.error("Error sending score:", error);
      }
    };

    const debouncedSendScore = debounce(sendScore, 3000);

    const sendScoreIfSignificantChange = () => {
      console.log(clickDelta);

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
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
  /* Add more styles for your icon */
}
</style>
