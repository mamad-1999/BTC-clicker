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
    height: 40%;
    display: flex;
    justify-content: center;
  }
  #bit{
    width: 200px;
    height: 200px;
    cursor: pointer;
    position: absolute;
  }

  #bit:active{
    width: 210px;
    height: 205px;
  }

  @media screen and (max-width: 400px) {
    #bit{
    width: 260px;
    height: 260px;
  }
  #bit:active{
    width: 270px;
    height: 265px;
  }
}
</style>