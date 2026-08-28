<template>
  <div class="home">
    <AppHeader />

    <HeroSection />

    <StudentHome v-if="authStore.isLoggedIn && authStore.isPersonal" />
    <EnterpriseHome v-else-if="authStore.isLoggedIn && authStore.isEnterprise" />
    <AdminHome v-else-if="authStore.isLoggedIn && authStore.isAdmin" />
    <template v-else>
      <section class="practice-section">
        <div class="section-header">
          <h2 class="section-title-left">行动进行时</h2>
          <div class="title-tag">最新发布</div>
        </div>

        <div class="practice-container">
          <ActivityList />
          <ImageCarousel />
        </div>
      </section>

      <StatsSection />
    </template>

    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import HeroSection from '@/components/home/HeroSection.vue'
import ActivityList from '@/components/home/ActivityList.vue'
import ImageCarousel from '@/components/home/ImageCarousel.vue'
import StatsSection from '@/components/home/StatsSection.vue'
import StudentHome from '@/components/home/StudentHome.vue'
import EnterpriseHome from '@/components/home/EnterpriseHome.vue'
import AdminHome from '@/components/home/AdminHome.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<style scoped>
.practice-section {
  padding: 50px 5%;
  background-color: var(--color-bg-card);
}

.section-header {
  margin-bottom: 25px;
  max-width: var(--max-width);
  margin-left: auto;
  margin-right: auto;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.section-title-left {
  font-size: 26px;
  color: var(--color-accent-dark);
  font-weight: 600;
  position: relative;
  padding-bottom: 10px;
  margin-bottom: 6px;
}

.section-title-left::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background-color: var(--color-accent);
}

.title-tag {
  color: var(--color-accent);
  font-weight: 500;
  background-color: var(--color-accent-light);
  padding: 4px 10px;
  border-radius: 18px;
  font-size: 12px;
}

.practice-container {
  display: flex;
  gap: 30px;
  max-width: var(--max-width);
  margin: 0 auto;
}

@media (max-width: 1200px) {
  .practice-container {
    max-width: 1100px;
    gap: 10px;
  }
}

@media (max-width: 1024px) {
  .practice-container {
    flex-direction: column;
    gap: 30px;
    max-width: 900px;
  }

  .practice-section {
    padding-bottom: 50px;
  }

  .section-header {
    max-width: 900px;
  }
}

@media (max-width: 768px) {
  .practice-section {
    padding: 40px 5%;
  }

  .section-header {
    margin-bottom: 20px;
  }

  .section-title-left {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .practice-section {
    padding: 30px 5%;
  }

  .section-title-left {
    font-size: 22px;
  }
}
</style>
