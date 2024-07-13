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
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  width: 100%;
  height: 100vh;
}
</style>