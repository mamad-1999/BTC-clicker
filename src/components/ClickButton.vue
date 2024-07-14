<!-- ClickButton.vue -->
<template>
  <div class="bit-wrapper">
    <img @click="$emit('click')" id="bit" src="../assets/Bit.png" alt="Bit">
  </div>
</template>

<script>
export default {
  name: 'ClickButton',
  emits: ['click'],
};
</script>

<style scoped>
  .bit-wrapper{
    width: 100%;
    display: flex;
    justify-content: center;
    padding: 5px;
  }
  #bit{
    width: 200px;
    height: 200px;
    cursor: pointer;
  }

  #bit:active{
    width: 210px;
  }

  @media screen and (max-width: 400px) {
    #bit{
    width: 260px;
  }
  #bit:active{
    width: 270px;
  }
}
</style>