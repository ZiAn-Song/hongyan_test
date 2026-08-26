<template>
  <div class="right-content">
    <div class="image-carousel">
      <div class="carousel-container">
        <div class="carousel-slides" :style="{ transform: `translateX(-${currentSlide * 100}%)` }">
          <div
            v-for="(slide, index) in slides"
            :key="index"
            class="carousel-slide"
            :style="{ backgroundImage: `url('${slide.image}')` }"
          >
            <div class="slide-content">
              <div class="slide-number">{{ slide.number }}</div>
              <div class="slide-text">{{ slide.title }}</div>
              <p class="slide-description">{{ slide.description }}</p>
            </div>
          </div>
        </div>
        <div class="carousel-controls">
          <div
            v-for="(slide, index) in slides"
            :key="index"
            class="carousel-dot"
            :class="{ active: currentSlide === index }"
            @click="goToSlide(index)"
          ></div>
        </div>
      </div>
    </div>

    <div class="progress-box">
      <div class="progress-header">
        <i class="fas fa-bullhorn"></i>
        <span>本周实践动态</span>
      </div>
      <div class="progress-list">
        <div class="progress-item" v-for="(item, idx) in progressList" :key="idx">
          <span class="progress-tag">{{ item.tag }}</span>
          <div class="progress-content">
            <div class="progress-title">{{ item.title }}</div>
            <div class="progress-meta">{{ item.team }} · {{ item.date }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const slides = [
  {
    number: '01',
    title: '实践成果展示',
    description: '展示团队在全国各地的实践成果与精彩瞬间，记录青年学子的成长历程',
    image: '/img/pic2.jpg'
  },
  {
    number: '02',
    title: '团队风采',
    description: '呈现各实践团队的工作场景、团队协作与项目进展，展现青春活力',
    image: '/img/pic2.jpg'
  },
  {
    number: '03',
    title: '地方特色',
    description: '记录实践地的风土人情、文化特色与发展需求，展现地域多样性',
    image: '/img/pic2.jpg'
  }
]

const progressList = [
  { tag: '调研', title: '完成泰安农业需求首轮访谈', team: '智农先锋', date: '09-01' },
  { tag: '合作', title: '与青岛文化馆达成数字化合作', team: '文旅筑梦', date: '08-20' },
  { tag: '报告', title: '远程诊疗系统调研报告初稿完成', team: '医护连心', date: '08-15' },
  { tag: '申报', title: '乡村微电网方案进入专家评审', team: '新能源小组', date: '08-10' },
]

const currentSlide = ref(0)
let timer = null

const goToSlide = (index) => {
  currentSlide.value = index
  resetTimer()
}

const startCarousel = () => {
  timer = setInterval(() => {
    currentSlide.value = (currentSlide.value + 1) % slides.length
  }, 3000)
}

const resetTimer = () => {
  if (timer) clearInterval(timer)
  startCarousel()
}

onMounted(() => {
  startCarousel()
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.right-content {
  flex: 1.5;
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding-left: 10px;
}

.image-carousel {
  background-color: #f8f9fa;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
  height: 380px;
  position: relative;
}

.carousel-container {
  height: 100%;
  position: relative;
  overflow: hidden;
}

.carousel-slides {
  display: flex;
  height: 100%;
  transition: transform 0.5s ease-in-out;
}

.carousel-slide {
  min-width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  color: white;
  font-size: 20px;
  padding: 20px;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
}

.carousel-slide::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4);
  z-index: 1;
}

.slide-content {
  position: relative;
  z-index: 2;
  text-align: center;
}

.slide-number {
  font-size: 68px;
  font-weight: 700;
  color: var(--color-accent);
  margin-bottom: 20px;
  text-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
}

.slide-text {
  font-size: 28px;
  color: white;
  font-weight: 600;
  margin-bottom: 15px;
  text-shadow: 0 2px 5px rgba(0, 0, 0, 0.7);
}

.slide-description {
  font-size: 16px;
  color: #f0f0f0;
  max-width: 80%;
  line-height: 1.5;
  margin: 0 auto;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.7);
}

.carousel-controls {
  position: absolute;
  bottom: 25px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  gap: 15px;
  z-index: 10;
}

.carousel-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s;
}

.carousel-dot.active {
  background-color: var(--color-accent);
  transform: scale(1.4);
}

.carousel-dot:hover {
  background-color: rgba(74, 144, 226, 0.8);
}

.progress-box {
  background-color: var(--color-bg-card, #fff);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  height: 200px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.progress-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 700;
  color: var(--color-accent-dark, #2c3e50);
  padding-bottom: 8px;
  border-bottom: 2px solid var(--color-accent, #4a90e2);
}

.progress-header i {
  color: var(--color-accent, #4a90e2);
}

.progress-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow-y: auto;
  flex: 1;
}

.progress-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.progress-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  color: #fff;
  background: var(--color-accent, #4a90e2);
  flex-shrink: 0;
  margin-top: 2px;
}

.progress-content {
  flex: 1;
}

.progress-title {
  font-size: 13px;
  color: #333;
  line-height: 1.4;
}

.progress-meta {
  font-size: 11px;
  color: #999;
  margin-top: 2px;
}

@media (max-width: 1200px) {
  .image-carousel {
    height: 350px;
  }
}

@media (max-width: 1024px) {
  .right-content {
    flex: 1;
    padding-left: 0;
  }

  .image-carousel {
    height: 320px;
  }

  .progress-box {
    height: auto;
    min-height: 180px;
  }
}

@media (max-width: 768px) {
  .image-carousel {
    height: 280px;
  }

  .slide-number {
    font-size: 52px;
  }

  .slide-text {
    font-size: 22px;
  }

  .slide-description {
    font-size: 14px;
  }

  .progress-box {
    padding: 16px;
  }
}

@media (max-width: 480px) {
  .image-carousel {
    height: 240px;
  }

  .slide-number {
    font-size: 44px;
  }

  .slide-text {
    font-size: 20px;
  }

  .slide-description {
    font-size: 13px;
  }

  .progress-box {
    padding: 14px;
    height: auto;
    min-height: 160px;
  }
}
</style>
