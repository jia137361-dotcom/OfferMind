<template>
  <div class="auth-page">
    <div class="auth-bg">
      <div class="bg-orb bg-orb-1"></div>
      <div class="bg-orb bg-orb-2"></div>
    </div>
    <div class="auth-card glass">
      <div class="logo-icon-login">O</div>
      <h2>OfferMind 职引</h2>
      <p class="subtitle">AI 模拟面试平台</p>
      <p class="desc">登录后继续你的面试训练</p>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <input v-model="email" type="email" placeholder="请输入邮箱" required />
        </div>
        <div class="form-group">
          <input v-model="password" type="password" placeholder="请输入密码" required />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" class="login-btn" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      <p class="auth-link">还没有账号？<router-link to="/register">立即注册</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { login } from '../api/auth'
import { getProfile } from '../api/user'

const router = useRouter()
const authStore = useAuthStore()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''; loading.value = true
  try {
    const data = await login(email.value, password.value)
    authStore.setAuth(data)
    try { const profile = await getProfile(); authStore.setUserInfo(profile) } catch (_) {}
    router.push('/dashboard')
  } catch (e) { error.value = e.message
  } finally { loading.value = false }
}
</script>

<style scoped>
.auth-page {
  display: flex; align-items: center; justify-content: center;
  min-height: 100vh; position: relative; overflow: hidden;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 40%, #0f172a 100%);
}
.auth-bg { position: absolute; inset: 0; overflow: hidden; }
.bg-orb { position: absolute; border-radius: 50%; filter: blur(100px); opacity: .25; }
.bg-orb-1 {
  width: 500px; height: 500px;
  background: var(--primary); top: -200px; right: -150px;
  animation: orbFloat 8s ease-in-out infinite;
}
.bg-orb-2 {
  width: 400px; height: 400px;
  background: var(--primary-blue); bottom: -150px; left: -100px;
  animation: orbFloat 10s ease-in-out infinite reverse;
}
@keyframes orbFloat {
  0%, 100% { transform: translate(0,0) scale(1); }
  33% { transform: translate(30px,-20px) scale(1.05); }
  66% { transform: translate(-20px,10px) scale(.95); }
}

.auth-card {
  width: 420px; padding: 42px; text-align: center;
  position: relative; z-index: 1;
  border-radius: 28px;
  background: rgba(255,255,255,0.88);
  backdrop-filter: blur(20px);
  box-shadow: 0 30px 80px rgba(15,23,42,0.28);
  border: 1px solid rgba(255,255,255,0.35);
}

.logo-icon-login {
  width: 48px; height: 48px; border-radius: 16px;
  background: linear-gradient(135deg, var(--primary), var(--primary-blue));
  color: #fff; display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 22px; margin: 0 auto 14px;
}

.auth-card h2 { font-size: 24px; font-weight: 800; color: var(--text); margin-bottom: 4px; }
.subtitle { color: var(--text-secondary); font-size: 14px; }
.desc { color: var(--text-muted); font-size: 13px; margin-bottom: 24px; margin-top: 4px; }

.form-group { margin-bottom: 14px; text-align: left; }
.form-group input {
  width: 100%; height: 46px; padding: 0 14px; border: 1px solid #E2E8F0;
  border-radius: 14px; font-size: 14px; outline: none; transition: all var(--transition);
  background: #F8FAFC;
}
.form-group input:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(109,93,251,.1); background: #fff; }
.error { color: #ef4444; font-size: 13px; margin-bottom: 12px; }

.login-btn {
  width: 100%; height: 48px; border: none; border-radius: 14px;
  font-size: 15px; font-weight: 700; color: #fff;
  background: linear-gradient(135deg, #7C3AED, var(--primary-blue));
  cursor: pointer; transition: all .3s;
  box-shadow: 0 14px 30px rgba(99,102,241,.35);
  font-family: inherit;
}
.login-btn:hover { transform: translateY(-2px); box-shadow: 0 20px 40px rgba(99,102,241,.45); }
.login-btn:disabled { opacity: .6; cursor: not-allowed; transform: none; }

.auth-link { margin-top: 20px; font-size: 14px; color: var(--text-muted); }
.auth-link a { color: var(--primary); font-weight: 600; }
</style>
