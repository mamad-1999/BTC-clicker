<template>
  <div v-if="show" class="modal">
    <div class="modal-content">
      <h2 class="label">Enter Your Username</h2>
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
      if (username.value) {
        try {
          let res = await axios.post("http://127.0.0.1:5000/create-user", {
            username: username.value.trim(),
          });

          emit("close", { username: res.data.username, id: res.data.id });
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
  gap: 20px;
}

.modal-content {
  background-color: #fefefe;
  padding: 20px;
  border: 1px solid #888;
  width: 330px;
  height: 280px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 15px;
  border-radius: 5px;
  box-shadow: 5px 5px 80px rgb(46, 46, 46);
}

.label {
  color: #666666;
}

input {
  width: 100%;
  padding: 15px;
  margin: 10px 0;
  border: 1px solid rgb(216, 216, 216);
  border-radius: 5px;
  font-size: 16px;
  box-shadow: 1px 1px 10px rgb(138, 138, 138);
}

button {
  width: 100%;
  padding: 15px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 16px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: background-color 0.25s;
  box-shadow: 1px 1px 10px rgb(138, 138, 138);
}

button:hover {
  background-color: #409743;
}
</style>
