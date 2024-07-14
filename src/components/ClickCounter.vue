<!-- ClickCounter.vue -->
<template>
  <canvas ref="counterCanvas" :width="canvasWidth" :height="canvasHeight"></canvas>
</template>

<script>
export default {
  name: 'ClickCounter',
  props: {
    clicks: Number,
    clickDelta: Number,
  },
  data() {
    return {
      canvasWidth: 300,
      canvasHeight: 100,
    };
  },
  methods: {
    formatLargeNumber(num) {
      if (num < 1000000) {
        return Math.floor(num).toLocaleString();
      } else {
        const millions = (num / 1000000).toFixed(2);
        return parseFloat(millions).toString() + 'M';
      }
    },
    drawCounter() {
      const canvas = this.$refs.counterCanvas;
      const ctx = canvas.getContext('2d');
      
      // Clear the canvas
      ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);
      
      // Set the font and color
      ctx.font = 'bold 50px Arial';
      ctx.fillStyle = 'aliceblue';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      
      // Draw the formatted number
      const formattedNumber = this.formatLargeNumber(this.clicks);
      ctx.fillText(formattedNumber, this.canvasWidth / 2, this.canvasHeight / 2);
    }
  },
  watch: {
    clicks() {
      this.drawCounter();
    }
  },
  mounted() {
    this.drawCounter();
    
    // Adjust canvas size for mobile devices
    const updateCanvasSize = () => {
      if (window.innerWidth <= 400) {
        this.canvasWidth = window.innerWidth;
        this.canvasHeight = 150;
        this.$nextTick(() => {
          const canvas = this.$refs.counterCanvas;
          const ctx = canvas.getContext('2d');
          ctx.font = 'bold 65px Arial';
          this.drawCounter();
        });
      }
    };
    
    window.addEventListener('resize', updateCanvasSize);
    updateCanvasSize();
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateCanvasSize);
  }
};
</script>

<style scoped>
canvas {
  display: block;
  margin: 0 auto;
}
</style>