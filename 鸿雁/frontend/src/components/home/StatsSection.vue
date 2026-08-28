<template>
  <section class="stats-section" ref="statsRef">
    <h2 @click="replayAnimation">平台实践成果</h2>
    <div class="stats-container">
      <div v-for="(stat, index) in stats" :key="index" class="stat-item">
        <div class="stat-number">{{ displayValues[index] }}</div>
        <div class="stat-label">{{ stat.label }}</div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const stats = [
  { target: 3000, label: '团队正在参与' },
  { target: 8000, label: '优秀实践团队' },
  { target: 10000, label: '实践地标、区域' },
  { target: 6000, label: '受益地区' }
]

const displayValues = ref(stats.map(() => '0+'))
const statsRef = ref(null)
let observer = null
let animationTimers = []

const animateNumber = (index, target, duration = 2500) => {
  const increment = target / (duration / 50)
  let current = 0

  const timer = setInterval(() => {
    current += increment
    if (current >= target) {
      displayValues.value[index] = target + '+'
      clearInterval(timer)
    } else {
      displayValues.value[index] = Math.floor(current) + '+'
    }
  }, 50)

  animationTimers.push(timer)
}

const startStatsAnimation = () => {
  animationTimers.forEach(t => clearInterval(t))
  animationTimers = []
  displayValues.value = stats.map(() => '0+')

  stats.forEach((stat, index) => {
    setTimeout(() => {
      animateNumber(index, stat.target, 2500)
    }, index * 300)
  })
}

const replayAnimation = () => {
  startStatsAnimation()
}

onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          startStatsAnimation()
          observer.unobserve(entry.target)
        }
      })
    },
    { threshold: 0.3 }
  )

  if (statsRef.value) {
    observer.observe(statsRef.value)
  }
})

onUnmounted(() => {
  animationTimers.forEach(t => clearInterval(t))
  if (observer) observer.disconnect()
})
</script>

<style scoped>
.stats-section {
  padding: 60px 5%;
  background: linear-gradient(135deg, var(--ink), #4a90e2);
  color: white;
  text-align: center;
}

.stats-section h2 {
  font-size: 30px;
  margin-bottom: 40px;
  font-weight: 600;
  cursor: pointer;
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 25px;
  max-width: var(--max-width);
  margin: 0 auto;
}

.stat-item {
  padding: 25px 15px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  transition: all 0.3s;
}

.stat-item:hover {
  transform: translateY(-6px);
  background-color: rgba(255, 255, 255, 0.15);
}

.stat-number {
  font-size: 40px;
  font-weight: 700;
  margin-bottom: 10px;
  color: #63b3ed;
}

.stat-label {
  font-size: 16px;
  opacity: 0.9;
}

@media (max-width: 768px) {
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .stats-container {
    grid-template-columns: 1fr;
    gap: 15px;
  }
}
</style>
