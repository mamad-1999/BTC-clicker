<!-- LeaderboardModal.vue -->
<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-content">
      <h2 class="board-title">Leaderboard</h2>
      <button class="close-button" @click="$emit('close')">×</button>
      <table v-if="leaderboard.length > 0">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Username</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(player, index) in leaderboard" :key="player?.id">
            <td class="rank-cell">
              <span v-if="index < 3" class="medal">
                <img
                  :src="getMedalImage(index)"
                  :alt="`${getMedalName(index)} medal`"
                />
              </span>
              <span class="rank" v-else>{{ index + 1 }}</span>
            </td>
            <td>{{ player?.username }}</td>
            <td>{{ player?.score }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>No leaderboard data available at the moment.</p>
    </div>
  </div>
</template>

<script>
import goldImage from "../assets/gold.png";
import silverImage from "../assets/silver.png";
import bronzeImage from "../assets/bronze.png";

export default {
  name: "LeaderboardModal",
  props: {
    show: Boolean,
    leaderboard: {
      type: Array,
      default: () => [],
    },
  },
  emits: ["close"],
  methods: {
    getMedalImage(index) {
      const medals = [goldImage, silverImage, bronzeImage];

      return medals[index];
    },
    getMedalName(index) {
      const names = ["Gold", "Silver", "Bronze"];
      return names[index];
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding-inline: 15px;
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  max-width: 500px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.board-title {
  margin-top: 0;
  margin-bottom: 16px;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 30px;
  background: none;
  border: none;
  cursor: pointer;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 10px;
  text-align: left;
  border-bottom: 2px solid rgb(255, 204, 0);
}

th {
  background-color: rgba(255, 213, 47, 0.4);
}

.rank-cell {
  width: 50px;
  text-align: center;
}

.rank {
  background-color: #e0e0e0;
  padding: 3px 7px;
  border-radius: 40%;
}

.medal {
  display: inline-block;
  width: 30px;
  height: 30px;
}

.medal img {
  width: 25px;
  height: 25px;
  object-fit: contain;
}

::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-thumb {
  background-color: #c2c2c2;
  border-radius: 30px;
}
</style>
