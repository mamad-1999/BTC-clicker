<!-- LeaderboardModal.vue -->
<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-content">
      <h2>Leaderboard</h2>
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
          <!-- @vue-skip -->
          <tr v-for="(player, index) in leaderboard" :key="player?.id">
            <td>{{ index + 1 }}</td>
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

h2 {
  margin-top: 0;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
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
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f2f2f2;
}
</style>
