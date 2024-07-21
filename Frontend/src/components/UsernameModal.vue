<template>
  <div v-if="show" class="modal">
    <div class="modal-content">
      <h2>Enter Your Username</h2>
      <input
        v-model="username"
        @keyup.enter="submitUsername"
        placeholder="Username"
      />
      <button @click="submitUsername">Submit</button>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import axios from "axios";

export default {
  name: "UsernameModal",
  props: {
    show: Boolean,
  },
  emits: ["close"],
  setup(props, { emit }) {
    const username = ref("");

    const submitUsername = async () => {
      if (username.value.trim()) {
        try {
          await axios.post("/create-user", { username: username.value });
          emit("close", username);
        } catch (error) {
          console.error("Error creating user:", error);
        }
      }
    };

    return {
      username,
      submitUsername,
    };
  },
};
</script>

<style scoped>
.modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #fefefe;
  padding: 20px;
  border: 1px solid #888;
  width: 300px;
  text-align: center;
}

input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
}

button {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
}
</style>
