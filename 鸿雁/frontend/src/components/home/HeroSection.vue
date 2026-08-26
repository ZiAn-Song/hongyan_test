<template>
  <section class="hero">
    <div class="text-container">
      <h2>连接地方需求 赋能边疆发展</h2>
      <p class="subtitle">云边端协同、产学研融合 助力边疆发展</p>
      <p class="description">以温和的坚守，在你选择的路上深深扎根，你的存在本身正改变着时代的风向</p>
    </div>
  </section>

  <div class="transition-section">
    <div class="transition-text"></div>
  </div>
</template>

<style scoped>
.hero {
  background: url('/img/pic1.jpg');
  background-size: cover;
  background-position: center calc(50% - 40px);
  color: white;
  padding: 100px 5% 80px 5%;
  text-align: center;
  height: 70vh;
  min-height: 500px;
  max-height: 800px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  margin-top: -100px;
}

.text-container {
  background-color: rgba(0, 0, 0, 0.5);
  padding: 40px;
  border-radius: 15px;
  max-width: 900px;
  margin: 0 auto;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.hero h2 {
  font-size: 42px;
  margin-bottom: 20px;
  font-weight: 700;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6);
  line-height: 1.2;
}

.hero .subtitle {
  font-size: 24px;
  margin-bottom: 30px;
  color: #ecf0f1;
  font-weight: 300;
  text-shadow: 0 1px 5px rgba(0, 0, 0, 0.6);
}

.hero .description {
    font-size: 18px;
    max-width: 800px;
    margin: 0 auto 30px;
    line-height: 1.8;
    font-style: italic;
    color: #dfe6e9;
    text-shadow: 0 1px 5px rgba(0, 0, 0, 0.6);
  }

  .cta-row {
    display: flex;
    justify-content: center;
    gap: 16px;
    flex-wrap: wrap;
  }

  .btn-primary {
    display: inline-block;
    padding: 12px 24px;
    background: var(--color-accent, #c8102e);
    color: #fff;
    border-radius: 10px;
    text-decoration: none;
    font-weight: 600;
    font-size: 15px;
    transition: transform 0.2s, opacity 0.2s;
  }

  .btn-primary:hover {
    transform: translateY(-2px);
    opacity: 0.9;
  }

.transition-section {
  background: linear-gradient(to bottom, #2c3e50, #f9f9f9);
  height: 70px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  color: white;
  padding: 0 5%;
}

@media (max-width: 1024px) {
  .hero {
    height: 60vh;
    min-height: 400px;
  }

  .hero h2 {
    font-size: 36px;
  }

  .hero .subtitle {
    font-size: 20px;
  }

  .hero .description {
    font-size: 17px;
  }

  .text-container {
    padding: 30px;
  }
}

@media (max-width: 768px) {
  .hero {
    height: 50vh;
    min-height: 350px;
    padding: 60px 5%;
  }

  .hero h2 {
    font-size: 32px;
  }

  .hero .subtitle {
    font-size: 18px;
    margin-bottom: 20px;
  }

  .hero .description {
    font-size: 16px;
    margin-bottom: 20px;
  }

  .text-container {
    padding: 25px;
  }

  .transition-section {
    height: 60px;
  }
}

@media (max-width: 480px) {
  .hero {
    height: 45vh;
    min-height: 300px;
    padding: 40px 5%;
  }

  .hero h2 {
    font-size: 26px;
  }

  .hero .subtitle {
    font-size: 16px;
  }

  .hero .description {
    font-size: 14px;
  }

  .text-container {
    padding: 20px;
  }

  .transition-section {
    height: 50px;
  }
}
</style>
