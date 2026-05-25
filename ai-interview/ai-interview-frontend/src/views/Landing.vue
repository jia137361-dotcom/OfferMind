<template>
  <div class="landing">
    <!-- Hero -->
    <section class="hero">
      <div class="hero-bg">
        <div class="hero-orb hero-orb-1"></div>
        <div class="hero-orb hero-orb-2"></div>
      </div>
      <div class="hero-content">
        <h1 class="hero-title">AI 模拟面试，助你拿下<span class="gradient-text"> Offer</span></h1>
        <p class="hero-desc">基于 RAG + Agent 的智能面试训练平台，真实岗位匹配 · 个性化出题 · 专业评分</p>
        <div class="hero-actions">
          <router-link to="/register" class="btn-primary hero-btn">免费体验</router-link>
          <a href="#features" class="btn-secondary hero-btn">了解更多</a>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section id="features" class="features">
      <div class="container">
        <h2 class="section-title" style="text-align:center;margin-bottom:8px">为什么选择 OfferMind？</h2>
        <p class="section-subtitle" style="text-align:center;margin-bottom:40px">完整的 AI 面试训练闭环，从简历到报告一站式完成</p>
        <div class="feature-grid">
          <div class="feature-card" v-for="f in features" :key="f.title">
            <div class="feature-icon">{{ f.icon }}</div>
            <h3 class="feature-title">{{ f.title }}</h3>
            <p class="feature-desc">{{ f.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <p>© 2026 OfferMind 职引 · AI Interview Coach</p>
    </footer>
  </div>
</template>

<script setup>
const features = [
  { icon: '📄', title: '简历智能解析', desc: '上传 PDF 简历，AI 自动提取技能、项目经历、教育背景，生成简历质量分析报告' },
  { icon: '🎯', title: 'AI 岗位匹配', desc: '基于 LangChain Agent 自动构建候选人画像，匹配最合适的岗位模板' },
  { icon: '💬', title: '真实模拟面试', desc: '针对岗位和简历个性化出题，涵盖技术、项目、系统设计等多维度' },
  { icon: '⚡', title: '实时流式评分', desc: '每道题即时获得 AI 评分与反馈，参考答案 + 关键得分点让评分有据可依' },
  { icon: '📊', title: '专业面试报告', desc: '综合评估报告包含评分、优劣势分析、改进建议和录用推荐' },
  { icon: '🧠', title: 'RAG 智能题库', desc: 'pgvector + DashScope Embedding 语义检索，精准匹配岗位相关题目' },
]
</script>

<style scoped>
.landing { min-height: 100vh; }

/* Hero */
.hero {
  position: relative; overflow: hidden;
  min-height: 520px; display: flex; align-items: center; justify-content: center;
  padding: 80px 24px;
}
.hero-bg { position: absolute; inset: 0; }
.hero-orb { position: absolute; border-radius: 50%; filter: blur(100px); opacity: .2; }
.hero-orb-1 {
  width: 600px; height: 600px; background: var(--primary);
  top: -200px; right: -200px; animation: orbFloat 10s ease-in-out infinite;
}
.hero-orb-2 {
  width: 400px; height: 400px; background: var(--primary-blue);
  bottom: -100px; left: -100px; animation: orbFloat 12s ease-in-out infinite reverse;
}
@keyframes orbFloat {
  0%, 100% { transform: translate(0,0) scale(1); }
  33% { transform: translate(30px,-20px) scale(1.05); }
  66% { transform: translate(-20px,10px) scale(.95); }
}

.hero-content { position: relative; text-align: center; max-width: 680px; z-index: 1; }
.hero-title { font-size: 42px; font-weight: 800; line-height: 1.2; color: var(--text); margin-bottom: 16px; }
.hero-desc { font-size: 17px; color: var(--text-secondary); line-height: 1.6; margin-bottom: 32px; }
.hero-actions { display: flex; gap: 14px; justify-content: center; }
.hero-btn { height: 48px; padding: 0 28px; border-radius: 14px; font-size: 15px; }

/* Features */
.features { padding: 80px 24px; }
.feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.feature-card {
  padding: 28px 24px; text-align: center;
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 20px; transition: all var(--transition);
  box-shadow: var(--shadow);
}
.feature-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }
.feature-icon { font-size: 36px; margin-bottom: 12px; }
.feature-title { font-size: 16px; font-weight: 700; color: var(--text); margin-bottom: 8px; }
.feature-desc { font-size: 13px; color: var(--text-secondary); line-height: 1.6; }

/* Footer */
.footer { text-align: center; padding: 32px; color: var(--text-muted); font-size: 13px; border-top: 1px solid var(--border); }
</style>
