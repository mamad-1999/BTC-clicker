<!-- ClickButton.vue -->
<template>
  <div class="bit-wrapper">
    <img @click="$emit('click')" id="bit" src="../assets/Bit.png" alt="Bit" />
  </div>
</template>

<script>
export default {
  name: "ClickButton",
  emits: ["click"],
};
</script>

<style scoped>
.bit-wrapper {
  width: 100%;
  padding: 5px;
  display: flex;
  justify-content: center;
}
#bit {
  width: 200px;
  height: 200px;
  cursor: pointer;
  filter: drop-shadow(2px 2px 20px rgba(64, 26, 0, 1));
}

#bit:active {
  width: 205px;
}

@media screen and (max-width: 400px) {
  #bit {
    width: 240px;
    height: 240px;
  }
  #bit:active {
    width: 245px;
  }
}
</style>
