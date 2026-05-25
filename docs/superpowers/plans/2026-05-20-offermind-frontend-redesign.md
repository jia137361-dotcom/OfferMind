# OfferMind 用户端前端重设计 — 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 渐进增强用户端前端 — 新增 Landing + InterviewNew 页面，改造 Dashboard/Interview/Report，后端零改动

**Architecture:** Vue 3 SPA，所有 API 复用现有后端接口。新增 2 个页面组件，改造 5 个，修改路由和导航栏

**Tech Stack:** Vue 3 (Composition API), Vue Router 4, Pinia, Axios, Vite 5, 纯 CSS (Inter 字体 + CSS 变量)

---

## Task 1: 添加 agentSetup API 函数

**Files:**
- Modify: `c:\py文档\ai-interview\ai-interview\ai-interview-frontend\src\api\interview.js`

- [ ] **Step 1: 在 interview.js 末尾添加 agentSetup 函数**

```js
export function agentSetup(resumeId) {
  return api.post('/interviews/agent-setup', { resume_id: resumeId })
}
```

- [ ] **Step 2: 确认 api/request.js 的 baseURL 配置正确**

无需修改，已有 `baseURL: '/api/v1'`，timeout 60s。

- [ ] **Step 3: 提交**

```bash
git add src/api/interview.js
git commit -m "feat: add agentSetup API function"
```

---

## Task 2: 更新路由 — 新增 Landing 和 InterviewNew，移除 ResumeUpload 导航

**Files:**
- Modify: `c:\py文档\ai-interview\ai-interview\ai-interview-frontend\src\router\index.js`

- [ ] **Step 1: 替换路由配置**

将现有路由替换为：

```js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  // 公开页面
  { path: '/', name: 'Landing', component: () => import('../views/Landing.vue') },
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
  { path: '/register', name: 'Register', component: () => import('../views/Register.vue') },

  // 需要登录
  { path: '/dashboard', name: 'Dashboard', component: () => import('../views/Dashboard.vue'), meta: { auth: true } },
  { path: '/interview/new', name: 'InterviewNew', component: () => import('../views/InterviewNew.vue'), meta: { auth: true } },
  { path: '/interview/:id', name: 'Interview', component: () => import('../views/Interview.vue'), meta: { auth: true } },
  { path: '/report/:id', name: 'Report', component: () => import('../views/Report.vue'), meta: { auth: true } },
  { path: '/profile', name: 'Profile', component: () => import('../views/Profile.vue'), meta: { auth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.auth && !authStore.isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
```

变化：
- 新增 `/` → Landing
- 新增 `/interview/new` → InterviewNew
- 移除 `/resume/upload` 路由
- `/interview/:id/report` → `/report/:id`
- 移除 `path: '/' redirect: '/dashboard'`

- [ ] **Step 2: 提交**

```bash
git add src/router/index.js
git commit -m "feat: add Landing and InterviewNew routes, simplify report route"
```

---

## Task 3: 更新 App.vue 导航栏 — 未登录/已登录双模式

**Files:**
- Modify: `c:\py文档\ai-interview\ai-interview\ai-interview-frontend\src\App.vue`

- [ ] **Step 1: 重写 App.vue**

完整替换为：

```vue
<template>
  <div id="app">
    <nav class="navbar" v-if="authStore.isLoggedIn">
      <div class="nav-content">
        <router-link to="/dashboard" class="logo">
          <div class="logo-icon">O</div>
          <div>
            <div class="logo-title">OfferMind 职引</div>
            <div class="logo-subtitle">AI Interview Coach</div>
          </div>
        </router-link>
        <div class="nav-links">
          <router-link to="/dashboard" class="nav-item" active-class="nav-active">工作台</router-link>
          <router-link to="/interview/new" class="nav-item" active-class="nav-active">新面试</router-link>
          <router-link to="/profile" class="nav-user-link">
            <img v-if="authStore.userAvatar && !avatarError" :src="authStore.userAvatar" class="nav-avatar" @error="avatarError = true" />
            <span v-else class="nav-avatar-placeholder">{{ (authStore.userName || 'U')[0] }}</span>
            <span>{{ authStore.userName || '个人中心' }}</span>
          </router-link>
          <button class="btn-secondary btn-sm" @click="logout">退出</button>
        </div>
      </div>
    </nav>

    <!-- 未登录导航 -->
    <nav class="navbar" v-else>
      <div class="nav-content">
        <router-link to="/" class="logo">
          <div class="logo-icon">O</div>
          <div>
            <div class="logo-title">OfferMind 职引</div>
            <div class="logo-subtitle">AI Interview Coach</div>
          </div>
        </router-link>
        <div class="nav-links">
          <router-link to="/login" class="nav-item">登录</router-link>
          <router-link to="/register" class="btn-primary btn-sm" style="color:#fff">免费注册</router-link>
        </div>
      </div>
    </nav>

    <router-view />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'
import { getProfile } from './api/user'

const authStore = useAuthStore()
const router = useRouter()
const avatarError = ref(false)

onMounted(async () => {
  if (authStore.token) {
    try { const data = await getProfile(); authStore.setUserInfo(data); avatarError.value = false } catch (e) {}
  }
})

function logout() { authStore.logout(); router.push('/') }
</script>

<style scoped>
.navbar {
  background: rgba(255,255,255,0.8);
  backdrop-filter: blur(16px) saturate(180%);
  border-bottom: 1px solid rgba(0,0,0,0.06);
  padding: 0 24px;
  position: sticky; top: 0; z-index: 100;
}
.nav-content {
  max-width: 1000px; margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between;
  height: 64px;
}

.logo { display: flex; align-items: center; gap: 10px; text-decoration: none; }
.logo-icon {
  width: 34px; height: 34px; border-radius: 12px;
  background: linear-gradient(135deg, var(--primary), var(--primary-blue));
  color: #fff; display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 16px; flex-shrink: 0;
}
.logo-title { font-size: 18px; font-weight: 700; color: #1E293B; line-height: 1.2; }
.logo-subtitle { font-size: 11px; color: #94A3B8; line-height: 1.2; }

.nav-links { display: flex; align-items: center; gap: 24px; font-size: 14px; }

.nav-item {
  color: var(--text-secondary); font-weight: 500; transition: color var(--transition);
  position: relative; text-decoration: none;
}
.nav-item:hover { color: var(--primary); }

.nav-active {
  color: var(--primary); font-weight: 700;
}
.nav-active::after {
  content: "";
  position: absolute; left: 50%; bottom: -20px;
  width: 24px; height: 3px; border-radius: 999px;
  background: linear-gradient(135deg, var(--primary), var(--primary-blue));
  transform: translateX(-50%);
}

.nav-user-link {
  display: flex; align-items: center; gap: 8px; color: var(--text-secondary); font-size: 13px;
  text-decoration: none;
}
.nav-user-link:hover { color: var(--primary); }
.nav-avatar { width: 32px; height: 32px; border-radius: 50%; object-fit: cover; }
.nav-avatar-placeholder {
  width: 32px; height: 32px; border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--primary-blue));
  color: #fff; display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 600;
}
</style>
```

变化：
- `v-if="authStore.isLoggedIn"` 替代原来的 `v-if="authStore.token"`
- 新增未登录导航栏（`v-else`），显示「登录」+「免费注册」
- 导航项文字：「面试记录」→「工作台」，「上传简历」→「新面试」
- 退出后跳转到 `/` 而不是 `/login`

- [ ] **Step 2: 提交**

```bash
git add src/App.vue
git commit -m "feat: dual-mode navbar for logged-in/logged-out states"
```

---

## Task 4: 新增 Landing.vue — 产品介绍页

**Files:**
- Create: `c:\py文档\ai-interview\ai-interview\ai-interview-frontend\src\views\Landing.vue`

- [ ] **Step 1: 创建 Landing.vue**

```vue
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
```

- [ ] **Step 2: 提交**

```bash
git add src/views/Landing.vue
git commit -m "feat: add Landing page with hero and features grid"
```

---

## Task 5: 新增 InterviewNew.vue — 快速/Agent 双模式面试创建

**Files:**
- Create: `c:\py文档\ai-interview\ai-interview\ai-interview-frontend\src\views\InterviewNew.vue`

- [ ] **Step 1: 创建 InterviewNew.vue**

```vue
<template>
  <div class="container" style="max-width:620px">
    <h1 class="section-title" style="margin-bottom:4px">创建新面试</h1>
    <p class="section-subtitle" style="margin-bottom:20px">选择面试模式，AI 将为你生成个性化面试题目</p>

    <!-- Tab 切换 -->
    <div class="tabs">
      <button :class="['tab', { active: mode === 'quick' }]" @click="mode = 'quick'">快速开始</button>
      <button :class="['tab', { active: mode === 'agent' }]" @click="mode = 'agent'">
        <span>🤖</span> Agent 智能匹配
      </button>
    </div>

    <!-- 快速模式 -->
    <div v-if="mode === 'quick'" class="card">
      <div class="form-group">
        <label>选择简历</label>
        <select v-model="selectedResumeId">
          <option :value="null" disabled>请选择已解析的简历</option>
          <option v-for="r in resumes" :key="r.resume_id" :value="r.resume_id" :disabled="r.status !== 'completed'">
            {{ r.file_name }} ({{ r.target_position }}) {{ r.status !== 'completed' ? '— 解析中' : '' }}
          </option>
        </select>
        <p class="form-hint" style="margin-top:8px;font-size:12px;color:var(--text-muted)">
          或 <router-link to="" @click.prevent="triggerUpload">上传新简历</router-link>
        </p>
        <input ref="fileInput" type="file" accept=".pdf" hidden @change="onUpload" />
      </div>
      <div class="form-group">
        <label>目标岗位</label>
        <input v-model="targetPosition" placeholder="例如：Python后端开发工程师" />
      </div>
      <div class="form-group">
        <label>难度</label>
        <div class="radio-row">
          <label v-for="d in difficulties" :key="d.value" :class="['radio-chip', { active: difficulty === d.value }]">
            <input type="radio" v-model="difficulty" :value="d.value" hidden />
            {{ d.label }}
          </label>
        </div>
      </div>
      <div class="form-group">
        <label>题目数量</label>
        <div class="radio-row">
          <label v-for="n in [3,5,8]" :key="n" :class="['radio-chip', { active: totalQuestions === n }]">
            <input type="radio" v-model="totalQuestions" :value="n" hidden />
            {{ n }} 题{{ n === 3 ? ' · 快速' : n === 5 ? ' · 标准' : ' · 深度' }}
          </label>
        </div>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
      <button class="btn-primary" style="width:100%" @click="startQuick" :disabled="!selectedResumeId || loading">
        {{ loading ? '准备中...' : '开始面试' }}
      </button>
    </div>

    <!-- Agent 模式 -->
    <div v-if="mode === 'agent'" class="card">
      <div class="tips-card">
        <div class="tips-icon">🤖</div>
        <div>
          <div class="tips-title">一键智能匹配</div>
          <div class="tips-desc">AI 将自动分析你的简历，构建候选人画像，匹配最合适岗位模板，生成个性化面试题目</div>
        </div>
      </div>
      <div class="form-group">
        <label>选择简历</label>
        <select v-model="selectedResumeId">
          <option :value="null" disabled>请选择已解析的简历</option>
          <option v-for="r in completedResumes" :key="r.resume_id" :value="r.resume_id">
            {{ r.file_name }} ({{ r.target_position }})
          </option>
        </select>
      </div>
      <p v-if="error" class="error">{{ error }}</p>
      <button class="btn-primary" style="width:100%" @click="startAgent" :disabled="!selectedResumeId || loading">
        {{ loading ? 'Agent 分析中...' : '开始智能面试' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getResumes, uploadResume } from '../api/resume'
import { startInterview, agentSetup } from '../api/interview'

const router = useRouter()
const mode = ref('quick')
const resumes = ref([])
const selectedResumeId = ref(null)
const targetPosition = ref('Python后端开发工程师')
const difficulty = ref('medium')
const totalQuestions = ref(5)
const loading = ref(false)
const error = ref('')
const fileInput = ref(null)

const difficulties = [
  { value: 'easy', label: '简单' },
  { value: 'medium', label: '中等' },
  { value: 'hard', label: '困难' },
]

const completedResumes = computed(() => resumes.value.filter(r => r.status === 'completed'))

onMounted(async () => {
  try { const data = await getResumes(); resumes.value = data.items || data
  } catch (e) { console.error(e) }
})

function triggerUpload() { fileInput.value?.click() }

async function onUpload(e) {
  const file = e.target.files[0]
  if (!file) return
  error.value = ''
  loading.value = true
  try {
    const data = await uploadResume(file, targetPosition.value)
    // 轮询等待解析完成
    let retries = 0
    while (retries < 30) {
      await new Promise(r => setTimeout(r, 2000))
      const { getResume } = await import('../api/resume')
      const detail = await getResume(data.resume_id)
      if (detail.status === 'completed') {
        resumes.value.unshift({ resume_id: data.resume_id, file_name: file.name, target_position: targetPosition.value, status: 'completed' })
        selectedResumeId.value = data.resume_id
        return
      }
      if (detail.status === 'failed') throw new Error('简历解析失败')
      retries++
    }
    throw new Error('解析超时')
  } catch (e) { error.value = e.message
  } finally { loading.value = false }
}

async function startQuick() {
  error.value = ''; loading.value = true
  try {
    const data = await startInterview({
      resume_id: selectedResumeId.value,
      target_position: targetPosition.value,
      difficulty: difficulty.value,
      total_questions: totalQuestions.value
    })
    router.push(`/interview/${data.interview_id}`)
  } catch (e) { error.value = e.message
  } finally { loading.value = false }
}

async function startAgent() {
  error.value = ''; loading.value = true
  try {
    const data = await agentSetup(selectedResumeId.value)
    if (data.success && data.interview_id) {
      router.push(`/interview/${data.interview_id}`)
    } else {
      // Agent 可能返回匹配结果但没有直接创建面试
      error.value = data.output || 'Agent 处理完成，请查看结果'
    }
  } catch (e) { error.value = e.message
  } finally { loading.value = false }
}
</script>

<style scoped>
.tabs { display: flex; gap: 8px; margin-bottom: 20px; }
.tab {
  flex: 1; padding: 12px; border-radius: 14px; font-size: 14px; font-weight: 600;
  background: #fff; color: var(--text-secondary); border: 1px solid var(--border);
  transition: all var(--transition); display: flex; align-items: center; justify-content: center; gap: 6px;
}
.tab:hover { border-color: var(--primary); color: var(--primary); }
.tab.active { background: var(--primary); color: #fff; border-color: var(--primary); box-shadow: 0 8px 20px rgba(99,102,241,.25); }

.form-group { margin-bottom: 16px; }
.form-hint a { color: var(--primary); font-weight: 500; }

.radio-row { display: flex; gap: 8px; }
.radio-chip {
  flex: 1; padding: 10px; border-radius: 12px; text-align: center;
  border: 1px solid var(--border); cursor: pointer; font-size: 13px; font-weight: 500;
  transition: all var(--transition); color: var(--text-secondary);
}
.radio-chip:hover { border-color: var(--primary); }
.radio-chip.active { background: var(--primary-light); color: var(--primary); border-color: var(--primary); font-weight: 700; }

.tips-card {
  display: flex; gap: 12px; padding: 16px; margin-bottom: 22px;
  border-radius: 18px;
  background: linear-gradient(135deg, #EEF2FF, #EFF6FF);
  border: 1px solid #DBEAFE;
}
.tips-icon { font-size: 24px; flex-shrink: 0; }
.tips-title { font-size: 15px; font-weight: 700; color: #1E293B; }
.tips-desc { margin-top: 4px; font-size: 13px; color: #64748B; }

.error { color: #ef4444; font-size: 13px; margin-bottom: 12px; }
</style>
```

- [ ] **Step 2: 提交**

```bash
git add src/views/InterviewNew.vue
git commit -m "feat: add InterviewNew page with Quick/Agent dual tab"
```

---

## Task 6: 改造 Dashboard.vue — 工作台风格

**Files:**
- Modify: `c:\py文档\ai-interview\ai-interview\ai-interview-frontend\src\views\Dashboard.vue`

- [ ] **Step 1: 完整替换 Dashboard.vue**

```vue
<template>
  <div class="container" style="max-width:900px">
    <!-- 问候 -->
    <div class="greeting">
      <h1 class="section-title">👋 你好，{{ userName }}</h1>
      <p class="section-subtitle">你的面试训练进度</p>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-row" v-if="!loading">
      <div class="stat-card">
        <div class="stat-icon">📋</div>
        <strong>{{ interviews.length }}</strong>
        <span>全部面试</span>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🔄</div>
        <strong>{{ inProgressCount }}</strong>
        <span>进行中</span>
      </div>
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <strong>{{ completedCount }}</strong>
        <span>已完成</span>
      </div>
      <div class="stat-card">
        <div class="stat-icon">⭐</div>
        <strong>{{ avgScore }}</strong>
        <span>平均分</span>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="quick-actions">
      <router-link to="/interview/new" class="btn-primary">+ 新面试</router-link>
      <router-link to="/interview/new" class="btn-secondary" @click="setAgentMode">🤖 Agent 智能匹配</router-link>
    </div>

    <!-- 面试列表 -->
    <div class="list-header">
      <h2 class="section-title" style="font-size:18px">最近面试</h2>
      <router-link to="" v-if="interviews.length > 5" style="font-size:13px">查看全部</router-link>
    </div>

    <div v-if="loading" class="empty-state">
      <div class="skeleton" style="width:100%;height:100px;margin-bottom:12px"></div>
      <div class="skeleton" style="width:100%;height:100px"></div>
    </div>

    <div v-else-if="interviews.length === 0" class="empty-state card">
      <div class="icon">🎯</div>
      <div class="title">还没有面试记录</div>
      <div class="desc">创建你的第一次 AI 模拟面试</div>
    </div>

    <div v-else class="interview-list">
      <div v-for="item in recentInterviews" :key="item.interview_id" class="card interview-card">
        <div class="card-top">
          <div class="card-left">
            <div class="card-title">{{ item.target_position }}</div>
            <div class="card-meta">AI 模拟面试 · {{ difficultyMap[item.difficulty] || item.difficulty }}难度 · {{ item.total_questions }} 题</div>
            <div class="card-date">{{ formatDate(item.created_at) }}</div>
          </div>
          <div class="card-right">
            <span :class="item.status === 'completed' ? 'status-done' : 'status-running'">
              {{ item.status === 'completed' ? '已完成' : '进行中' }}
            </span>
            <span v-if="item.overall_score" class="card-score">{{ item.overall_score }} 分</span>
          </div>
        </div>
        <div class="card-actions">
          <router-link v-if="item.status === 'in_progress'" :to="`/interview/${item.interview_id}`" class="btn-primary btn-sm">继续面试</router-link>
          <router-link v-else :to="`/report/${item.interview_id}`" class="btn-secondary btn-sm">查看报告</router-link>
          <button class="btn-danger btn-sm" @click="handleDelete(item.interview_id)">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { getInterviews, deleteInterview } from '../api/interview'

const authStore = useAuthStore()
const interviews = ref([])
const loading = ref(true)
const difficultyMap = { easy: '简单', medium: '中等', hard: '困难' }

const userName = computed(() => authStore.userName || '用户')
const inProgressCount = computed(() => interviews.value.filter(i => i.status === 'in_progress').length)
const completedCount = computed(() => interviews.value.filter(i => i.status === 'completed').length)
const avgScore = computed(() => {
  const done = interviews.value.filter(i => i.status === 'completed' && i.overall_score)
  if (!done.length) return '--'
  return (done.reduce((s, i) => s + i.overall_score, 0) / done.length).toFixed(1)
})
const recentInterviews = computed(() => interviews.value.slice(0, 5))

function formatDate(str) {
  if (!str) return ''
  return new Date(str).toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

onMounted(async () => {
  try { const data = await getInterviews(); interviews.value = data.items || []
  } catch (e) { console.error(e) } finally { loading.value = false }
})

async function handleDelete(id) {
  if (!confirm('确定删除？')) return
  try { await deleteInterview(id); interviews.value = interviews.value.filter(i => i.interview_id !== id)
  } catch (e) { alert('删除失败: ' + e.message) }
}
</script>

<style scoped>
.greeting { margin-bottom: 24px; }

.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
.stat-card {
  padding: 20px; border-radius: 20px; background: #fff;
  border: 1px solid var(--border); box-shadow: 0 16px 40px rgba(15,23,42,0.06);
  text-align: center;
}
.stat-icon { font-size: 24px; margin-bottom: 8px; }
.stat-card strong { display: block; font-size: 28px; font-weight: 800; color: var(--text); }
.stat-card span { font-size: 13px; color: var(--text-secondary); }

.quick-actions { display: flex; gap: 10px; margin-bottom: 28px; }

.list-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }

.interview-list { display: flex; flex-direction: column; gap: 12px; }
.interview-card { padding: 22px 24px; border-radius: 22px; }
.interview-card:hover { transform: translateY(-2px); box-shadow: 0 24px 60px rgba(15,23,42,0.10); }

.card-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; }
.card-title { font-size: 17px; font-weight: 800; color: var(--text); margin-bottom: 4px; }
.card-meta { font-size: 13px; color: var(--text-secondary); }
.card-date { font-size: 12px; color: var(--text-muted); margin-top: 4px; }
.card-right { display: flex; align-items: center; gap: 12px; flex-shrink: 0; }
.card-score { font-size: 15px; font-weight: 700; color: var(--primary); }
.card-actions { display: flex; gap: 8px; }
</style>
```

- [ ] **Step 2: 提交**

```bash
git add src/views/Dashboard.vue
git commit -m "feat: redesign Dashboard as workspace with stats and quick actions"
```

---

## Task 7: 改造 Interview.vue — 评分卡片 + 进度条

**Files:**
- Modify: `c:\py文档\ai-interview\ai-interview\ai-interview-frontend\src\views\Interview.vue`

- [ ] **Step 1: 在现有 Interview.vue 的顶部添加进度条**

在 template 最顶部（`.chat-container` 内）的 `.chat-header` 区域添加：

```html
<div class="interview-progress">
  <button class="back-btn" @click="goBack">← 返回</button>
  <div class="progress-info">
    <span>第 {{ currentIndex + 1 }} / {{ totalQuestions }} 题</span>
    <span class="progress-difficulty">{{ difficultyMap[difficulty] || '中等' }}</span>
  </div>
  <div class="progress-bar-wrapper">
    <div class="progress-bar" :style="{ width: progressPercent + '%' }"></div>
  </div>
</div>
```

在 script setup 中添加：

```js
import { useRouter } from 'vue-router'
const router = useRouter()
const difficulty = ref('medium')
const totalQuestions = ref(5)
const difficultyMap = { easy: '简单', medium: '中等', hard: '困难' }

// 从 messages 中获取面试信息
const currentIndex = computed(() => {
  // 根据已有消息计算当前题号
  const answered = messages.value.filter(m => m.role === 'candidate').length
  return Math.min(answered, totalQuestions.value - 1)
})
const progressPercent = computed(() => 
  totalQuestions.value > 0 ? Math.round((currentIndex.value / totalQuestions.value) * 100) : 0
)

function goBack() {
  if (confirm('确定离开？面试进度将保留。')) {
    router.push('/dashboard')
  }
}
```

- [ ] **Step 2: 评分卡片动画**

在每道题答完后，评分结果以卡片形式显示（替代纯文本）。修改消息渲染部分，在 candidate 消息后如果有 score，渲染：

```html
<div v-if="msg.score !== null && msg.score !== undefined && msg.role === 'candidate'" class="score-card">
  <div class="score-badge" :class="scoreLevel(msg.score)">
    ⭐ {{ msg.score }}
  </div>
  <div class="score-feedback">{{ msg.feedback }}</div>
  <div class="score-hint" v-if="msg.feedback && msg.feedback.includes('关键得分点')">
    {{ msg.feedback.includes('关键得分点') ? '基于参考答案对比评分' : '' }}
  </div>
</div>
```

添加辅助函数：

```js
function scoreLevel(s) {
  if (s >= 8) return 'score-high'
  if (s >= 6) return 'score-mid'
  return 'score-low'
}
```

评分卡片样式：

```css
.score-card {
  max-width: 70%; margin: 8px 0 8px auto; padding: 14px 18px;
  border-radius: 16px; background: linear-gradient(135deg, #f8f7ff, #f0f0ff);
  border: 1px solid #e0dffc; animation: scoreIn .4s ease;
}
@keyframes scoreIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.score-badge { font-size: 16px; font-weight: 800; margin-bottom: 6px; }
.score-high { color: #059669; }
.score-mid { color: #d97706; }
.score-low { color: #dc2626; }
.score-feedback { font-size: 13px; color: var(--text-secondary); line-height: 1.5; }
.score-hint { font-size: 11px; color: var(--text-muted); margin-top: 6px; }
```

- [ ] **Step 3: 提交**

```bash
git add src/views/Interview.vue
git commit -m "feat: add progress bar and score cards to Interview page"
```

---

## Task 8: 改造 Report.vue — 总分大卡 + 三栏 + 逐题进度条

**Files:**
- Modify: `c:\py文档\ai-interview\ai-interview\ai-interview-frontend\src\views\Report.vue`

- [ ] **Step 1: 重写 Report.vue 模板和样式**

完整替换为：

```vue
<template>
  <div class="container" style="max-width:780px">
    <router-link to="/dashboard" class="back-link">← 返回工作台</router-link>

    <div v-if="loading" class="empty-state"><p>加载中...</p></div>
    <div v-else-if="!report" class="empty-state card">
      <div class="icon">📊</div>
      <div class="title">报告加载失败</div>
    </div>

    <template v-else>
      <!-- 总分卡片 -->
      <div class="score-hero card">
        <div class="score-circle" :class="scoreLevel(report.overall_score)">
          <span class="score-num">{{ report.overall_score }}</span>
          <span class="score-label">{{ scoreLabel(report.overall_score) }}</span>
        </div>
        <div class="score-info">
          <h1 class="section-title">面试报告</h1>
          <p class="score-meta">{{ interviewInfo }}</p>
          <p class="hire-badge" v-if="report.report?.hire_recommendation">
            {{ report.report.hire_recommendation }}
          </p>
        </div>
      </div>

      <!-- 总体评价 -->
      <div class="card" v-if="report.report?.summary" style="margin-top:16px">
        <h3 style="font-size:16px;font-weight:700;margin-bottom:8px">总体评价</h3>
        <p style="font-size:14px;color:var(--text-secondary);line-height:1.7">{{ report.report.summary }}</p>
      </div>

      <!-- 三栏 -->
      <div class="three-col" v-if="report.report">
        <div class="col-card strengths">
          <h4>✅ 优势</h4>
          <ul><li v-for="s in (report.report.strengths || [])" :key="s">{{ s }}</li></ul>
        </div>
        <div class="col-card weaknesses">
          <h4>🔧 待改进</h4>
          <ul><li v-for="w in (report.report.weaknesses || [])" :key="w">{{ w }}</li></ul>
        </div>
        <div class="col-card suggestions">
          <h4>💡 建议</h4>
          <ul><li v-for="s in (report.report.suggestions || [])" :key="s">{{ s }}</li></ul>
        </div>
      </div>

      <!-- 逐题回顾 -->
      <div class="card" v-if="report.report?.question_scores?.length" style="margin-top:16px">
        <h3 style="font-size:16px;font-weight:700;margin-bottom:16px">逐题回顾</h3>
        <div class="question-item" v-for="(qs, i) in report.report.question_scores" :key="i">
          <div class="q-header">
            <span class="q-index">Q{{ i + 1 }}</span>
            <span class="q-text">{{ qs.question }}</span>
            <span class="q-score" :class="scoreLevel(qs.score)">{{ qs.score }} 分</span>
          </div>
          <div class="q-bar-wrapper">
            <div class="q-bar" :style="{ width: (qs.score * 10) + '%' }" :class="scoreLevel(qs.score)"></div>
          </div>
        </div>
      </div>

      <!-- 操作 -->
      <div class="actions">
        <router-link to="/interview/new" class="btn-primary">再来一次</router-link>
        <router-link to="/dashboard" class="btn-secondary">查看面试记录</router-link>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { getReport } from '../api/interview'
import { getInterviews } from '../api/interview'

const route = useRoute()
const report = ref(null)
const loading = ref(true)
const interviewInfo = ref('')

function scoreLevel(s) {
  if (s >= 8) return 'score-high'
  if (s >= 6) return 'score-mid'
  return 'score-low'
}
function scoreLabel(s) {
  if (s >= 9) return '优秀'
  if (s >= 8) return '良好'
  if (s >= 6) return '一般'
  return '需努力'
}

onMounted(async () => {
  try {
    const id = route.params.id
    const data = await getReport(id)
    report.value = data

    // 获取面试元信息
    const list = await getInterviews()
    const item = (list.items || []).find(i => i.interview_id === parseInt(id))
    if (item) {
      const diffMap = { easy: '简单', medium: '中等', hard: '困难' }
      interviewInfo.value = `${item.target_position} · ${diffMap[item.difficulty] || item.difficulty} · ${item.total_questions} 题`
    }
  } catch (e) { console.error(e)
  } finally { loading.value = false }
})
</script>

<style scoped>
.back-link { display: inline-block; margin-bottom: 16px; font-size: 14px; color: var(--text-secondary); }

.score-hero { display: flex; align-items: center; gap: 24px; padding: 28px; }
.score-circle {
  width: 100px; height: 100px; border-radius: 50%;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  color: #fff; flex-shrink: 0;
}
.score-circle.score-high { background: linear-gradient(135deg, #10b981, #34d399); }
.score-circle.score-mid { background: linear-gradient(135deg, var(--primary), var(--primary-blue)); }
.score-circle.score-low { background: linear-gradient(135deg, #f59e0b, #f97316); }
.score-num { font-size: 32px; font-weight: 800; line-height: 1; }
.score-label { font-size: 12px; opacity: .85; margin-top: 2px; }

.score-info { flex: 1; }
.score-meta { font-size: 13px; color: var(--text-muted); margin-top: 4px; }
.hire-badge { display: inline-block; margin-top: 8px; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 700; background: var(--primary-light); color: var(--primary); }

.three-col { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 16px; }
.col-card { padding: 18px; border-radius: 16px; border: 1px solid var(--border); background: #fff; }
.col-card h4 { font-size: 14px; font-weight: 700; margin-bottom: 10px; }
.col-card ul { list-style: none; padding: 0; }
.col-card li { font-size: 13px; color: var(--text-secondary); line-height: 1.7; padding-left: 12px; position: relative; }
.col-card li::before { content: '•'; position: absolute; left: 0; color: var(--text-muted); }

.question-item { margin-bottom: 14px; }
.q-header { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
.q-index {
  width: 26px; height: 26px; border-radius: 8px; background: #f1f5f9;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700; color: var(--text-secondary); flex-shrink: 0;
}
.q-text { flex: 1; font-size: 13px; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.q-score { font-size: 14px; font-weight: 700; flex-shrink: 0; }
.q-score.score-high { color: #059669; }
.q-score.score-mid { color: #d97706; }
.q-score.score-low { color: #dc2626; }

.q-bar-wrapper { height: 6px; background: #f1f5f9; border-radius: 3px; overflow: hidden; }
.q-bar { height: 100%; border-radius: 3px; transition: width .6s ease; }
.q-bar.score-high { background: linear-gradient(90deg, #10b981, #34d399); }
.q-bar.score-mid { background: linear-gradient(90deg, var(--primary), var(--primary-blue)); }
.q-bar.score-low { background: linear-gradient(90deg, #f59e0b, #f97316); }

.actions { display: flex; gap: 10px; justify-content: center; margin-top: 28px; }
</style>
```

- [ ] **Step 2: 提交**

```bash
git add src/views/Report.vue
git commit -m "feat: redesign Report with score hero, three-column layout, and question timeline"
```

---

## Task 9: 微调 Register.vue 和 Profile.vue

**Files:**
- Modify: `c:\py文档\ai-interview\ai-interview\ai-interview-frontend\src\views\Register.vue`
- Modify: `c:\py文档\ai-interview\ai-interview\ai-interview-frontend\src\views\Profile.vue`

- [ ] **Step 1: Register.vue — 同步 Login 的玻璃卡片风格**

将 Register 的 `.auth-card` 改为与 Login 一致的玻璃卡片样式：

```css
.auth-card {
  border-radius: 28px;
  background: rgba(255,255,255,0.88);
  backdrop-filter: blur(20px);
  box-shadow: 0 30px 80px rgba(15,23,42,0.28);
  border: 1px solid rgba(255,255,255,0.35);
}
```

并将标题改为 "创建 OfferMind 账号"。

- [ ] **Step 2: Profile.vue — 继承全局样式即可**

Profile 页已使用 `.card` 和 `.container` 全局类，改造后自动继承新设计系统。无需模板改动，只需确认样式兼容。

- [ ] **Step 3: 提交**

```bash
git add src/views/Register.vue src/views/Profile.vue
git commit -m "style: sync Register and Profile with OfferMind design system"
```

---

## Task 10: 最终验证

- [ ] **Step 1: 确认 Vite 无编译错误**

Run: 访问 `http://localhost:3000`，检查浏览器控制台无红色报错

- [ ] **Step 2: 验证页面流转**

未登录时访问 `/` → Landing 页 → 点击「免费注册」→ Register → 登录 → Dashboard 工作台 → 「新面试」→ InterviewNew → 快速模式开始面试 → 答题 → 报告

- [ ] **Step 3: 验证 Agent 模式**

在 InterviewNew 页切换到 Agent Tab → 选择简历 → 「开始智能面试」

- [ ] **Step 4: 提交**

```bash
git add -A
git commit -m "chore: final verification, minor style tweaks"
```

---

## 自检

- **Spec coverage**: Landing (Task 4), InterviewNew (Task 5), Dashboard (Task 6), Interview (Task 7), Report (Task 8), App.vue (Task 3), Router (Task 2), Register/Profile (Task 9), API (Task 1)
- **无占位符**: 所有代码完整，无 TBD/TODO
- **类型一致性**: 所有组件使用相同的 Vue 3 Composition API 模式，API 函数签名与现有代码一致
