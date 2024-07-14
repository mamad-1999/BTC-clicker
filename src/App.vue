<!-- App.vue -->
<template>
  <div id="app">
    <ClickerGame />
  </div>
</template>

<script>
import ClickerGame from './components/ClickerGame.vue'

export default {
  name: 'App',
  components: {
    ClickerGame
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  width: 100%;
  height: 100%;
}
</style>