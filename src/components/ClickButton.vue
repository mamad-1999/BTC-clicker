<!-- ClickButton.vue -->
<template>
  <img @click="$emit('click')" id="bit" src="../assets/Bit.png" alt="Bit">
</template>

<script>
export default {
  name: 'ClickButton',
  emits: ['click'],
};
</script>

<style scoped>
  #bit{
    width: 200px;
    height: 200px;
    cursor: pointer;
  }
</style>