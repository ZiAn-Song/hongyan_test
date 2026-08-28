<template>
  <section class="hero">
    <div class="hero-inner">
      <p class="hero-kicker">东西部协作 · 对口支援 · 智能对接</p>
      <h2>当边疆需求遇上<em>内地供给</em><br>三级漏斗给出确定性答案</h2>
      <p class="subtitle">需求理解 · 三级漏斗匹配 · 大模型研判 · 历史范式参考</p>
      <div class="hero-actions">
        <router-link to="/demand" class="hero-btn primary">进入需求大厅</router-link>
        <router-link to="/achievement" class="hero-btn ghost">成果展示</router-link>
      </div>
      <div class="hero-stats">
        <span><b>51</b>边疆需求</span>
        <span class="div"></span>
        <span><b>36</b>内地供给</span>
        <span class="div"></span>
        <span><b>48</b>山大人才</span>
        <span class="div"></span>
        <span><b>55</b>成果范式</span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  background: var(--paper);
  padding: 72px 4% 60px;
  position: relative;
  overflow: hidden;
}
/* 极淡网格底纹（编辑风材质） */
.hero::before {
  content: "";
  position: absolute; inset: 0; z-index: 0;
  background:
    radial-gradient(ellipse 620px 380px at 12% -10%, rgba(30, 58, 110, 0.06), transparent),
    radial-gradient(ellipse 520px 340px at 92% 4%, rgba(163, 58, 42, 0.04), transparent),
    linear-gradient(rgba(28, 25, 23, 0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(28, 25, 23, 0.025) 1px, transparent 1px);
  background-size: auto, auto, 44px 44px, 44px 44px;
}

.hero-inner {
  position: relative; z-index: 1;
  max-width: var(--max-width);
  margin: 0 auto;
  text-align: center;
}

.hero-kicker {
  font-size: 11.5px;
  letter-spacing: 5px;
  color: var(--color-accent);
  font-weight: 700;
  margin-bottom: 18px;
}

.hero h2 {
  font-family: var(--font-serif);
  font-size: clamp(30px, 4.6vw, 46px);
  line-height: 1.5;
  letter-spacing: 2px;
  color: var(--ink);
  font-weight: 700;
}
.hero h2 em {
  font-style: normal;
  color: var(--color-primary);
  border-bottom: 3px solid rgba(30, 58, 110, 0.25);
}

.subtitle {
  margin-top: 18px;
  font-size: 14px;
  letter-spacing: 4px;
  color: var(--ink-3);
}

.hero-actions {
  margin-top: 34px;
  display: flex;
  gap: 14px;
  justify-content: center;
  flex-wrap: wrap;
}
.hero-btn {
  padding: 11px 34px;
  font-size: 14px;
  letter-spacing: 2px;
  border-radius: var(--radius-sm);
  transition: transform 0.25s var(--ease-out), box-shadow 0.25s var(--ease-out),
              background 0.2s, color 0.2s;
}
.hero-btn.primary {
  background: var(--color-primary);
  color: #fff;
  font-weight: 650;
}
.hero-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(30, 58, 110, 0.26);
  background: var(--color-primary-dark);
}
.hero-btn.ghost {
  border: 1px solid var(--rule);
  color: var(--ink-2);
}
.hero-btn.ghost:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  transform: translateY(-2px);
}

.hero-stats {
  margin-top: 44px;
  display: inline-flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
  justify-content: center;
  font-size: 12px;
  letter-spacing: 2px;
  color: var(--ink-3);
  padding: 12px 28px;
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}
.hero-stats b {
  font-family: Georgia, var(--font-mono);
  font-size: 19px;
  color: var(--color-primary);
  margin-right: 6px;
  font-weight: 700;
}
.hero-stats .div { width: 1px; height: 14px; background: var(--rule); }
</style>
