<template>
  <div class="login-page">
    <div class="login-bg">
      <div class="bg-orb bg-orb-1"></div>
      <div class="bg-orb bg-orb-2"></div>
    </div>
    <div class="login-card glass">
      <div class="logo-mark">◆</div>
      <h2 class="gradient-text">智面后台</h2>
      <p class="subtitle">系统管理</p>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="email" type="email" required />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input v-model="password" type="password" placeholder="请输入密码" required />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" class="btn-glow" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { authApi } from '../api'

const router = useRouter()
const authStore = useAuthStore()
const email = ref('admin@ai-interview.com')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''; loading.value = true
  try {
    const data = await authApi.login(email.value, password.value)
    authStore.setAuth({ ...data, email: email.value })
    router.push('/')
  } catch (e) { error.value = e.message }
  finally { loading.value = false }
}
</script>

<style scoped>
.login-page {
  display: flex; align-items: center; justify-content: center;
  min-height: 100vh; position: relative; overflow: hidden;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 40%, #0f172a 100%);
}
.login-bg { position: absolute; inset: 0; overflow: hidden; }
.bg-orb { position: absolute; border-radius: 50%; filter: blur(80px); opacity: .25; }
.bg-orb-1 {
  width: 500px; height: 500px;
  background: var(--primary); top: -200px; right: -150px;
  animation: orbFloat 8s ease-in-out infinite;
}
.bg-orb-2 {
  width: 400px; height: 400px;
  background: #8b5cf6; bottom: -150px; left: -100px;
  animation: orbFloat 10s ease-in-out infinite reverse;
}
@keyframes orbFloat {
  0%, 100% { transform: translate(0,0) scale(1); }
  33% { transform: translate(30px,-20px) scale(1.05); }
  66% { transform: translate(-20px,10px) scale(.95); }
}

.login-card {
  width: 400px; padding: 40px 36px; text-align: center;
  position: relative; z-index: 1;
}
.logo-mark { font-size: 28px; color: var(--primary); margin-bottom: 8px; }
.login-card h2 { font-size: 26px; font-weight: 800; margin-bottom: 2px; }
.subtitle { color: var(--text-muted); font-size: 13px; margin-bottom: 28px; }
.form-group { margin-bottom: 16px; text-align: left; }
.form-group label { display: block; margin-bottom: 6px; font-size: 13px; font-weight: 600; color: var(--text-secondary); }
.form-group input { width: 100%; padding: 12px 14px; border: 1px solid var(--border); border-radius: var(--radius-xs); font-size: 14px; outline: none; transition: all var(--transition); background: #f8fafc; }
.form-group input:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(99,102,241,.1); background: #fff; }
.error { color: #ef4444; font-size: 13px; margin-bottom: 12px; }

.btn-glow {
  width: 100%; padding: 13px; border: none; border-radius: var(--radius-xs);
  font-size: 15px; font-weight: 600; color: #fff;
  background: linear-gradient(135deg, var(--primary), #8b5cf6, var(--accent));
  background-size: 200% 200%;
  animation: gradientShift 4s ease infinite;
  cursor: pointer; transition: all .3s;
  box-shadow: 0 4px 20px rgba(99,102,241,.35);
}
.btn-glow:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(99,102,241,.5); }
.btn-glow:disabled { opacity: .6; cursor: not-allowed; transform: none; }
@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
</style>
