<template>
  <div id="app">
    <nav class="navbar" v-if="authStore.token">
      <div class="nav-content">
        <router-link to="/dashboard" class="logo">
          <div class="logo-icon">O</div>
          <div>
            <div class="logo-title">OfferMind 职引</div>
            <div class="logo-subtitle">AI Interview Coach</div>
          </div>
        </router-link>
        <div class="nav-links">
          <router-link to="/dashboard" class="nav-item" active-class="nav-active">面试记录</router-link>
          <router-link to="/resume/upload" class="nav-item" active-class="nav-active">上传简历</router-link>
          <router-link to="/profile" class="nav-user-link">
            <img v-if="authStore.userAvatar && !avatarError" :src="authStore.userAvatar" class="nav-avatar" alt="avatar" @error="avatarError = true" />
            <span v-else class="nav-avatar-placeholder">{{ (authStore.userName || 'U')[0] }}</span>
            <span>{{ authStore.userName || '个人中心' }}</span>
          </router-link>
          <button class="btn-secondary btn-sm" @click="logout">退出</button>
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

function logout() { authStore.logout(); router.push('/login') }
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
  position: relative;
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
