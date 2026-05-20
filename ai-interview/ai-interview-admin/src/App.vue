<template>
  <div class="admin-layout" v-if="authStore.isLoggedIn">
    <aside class="sidebar">
      <div class="sidebar-logo">
        <span class="logo-icon">◆</span>
        <span class="logo-text gradient-text">智面</span>
      </div>
      <div class="sidebar-subtitle">后台管理</div>
      <nav class="sidebar-nav">
        <router-link to="/" exact-active-class="active">
          <span class="nav-dot"></span> 数据概览
        </router-link>
        <router-link to="/users" active-class="active">
          <span class="nav-dot"></span> 用户管理
        </router-link>
        <router-link to="/interviews" active-class="active">
          <span class="nav-dot"></span> 面试记录
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="admin-email">{{ authStore.email }}</div>
        <button class="logout-btn" @click="logout">退出登录</button>
      </div>
    </aside>
    <main class="main-content">
      <router-view />
    </main>
  </div>
  <router-view v-else />
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'
const authStore = useAuthStore()
const router = useRouter()
function logout() { authStore.logout(); router.push('/login') }
</script>

<style scoped>
.admin-layout { display: flex; min-height: 100vh; }

.sidebar {
  width: 240px;
  background: linear-gradient(180deg, #0f172a 0%, #1a1035 40%, #0f172a 100%);
  color: #fff; padding: 28px 18px;
  display: flex; flex-direction: column;
  position: fixed; top: 0; left: 0; bottom: 0; z-index: 50;
}

.sidebar::before {
  content: '';
  position: absolute; top: -50%; left: -50%;
  width: 200%; height: 200%;
  background:
    radial-gradient(ellipse at 25% 15%, rgba(99,102,241,.12) 0%, transparent 50%),
    radial-gradient(ellipse at 75% 85%, rgba(6,182,212,.08) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 50%, rgba(139,92,246,.06) 0%, transparent 60%);
  animation: auroraFloat 10s ease-in-out infinite; pointer-events: none;
}

@keyframes auroraFloat {
  0%, 100% { transform: translate(0,0) rotate(0deg); }
  33% { transform: translate(1%,-2%) rotate(.5deg); }
  66% { transform: translate(-1%,1%) rotate(-.5deg); }
}

.sidebar-logo {
  font-size: 22px; font-weight: 800; letter-spacing: -0.5px;
  display: flex; align-items: center; gap: 8px; position: relative;
}
.logo-icon { color: var(--primary); font-size: 20px; }

.sidebar-subtitle {
  font-size: 11px; color: #64748b; text-transform: uppercase;
  letter-spacing: 2px; margin: 4px 0 36px; position: relative;
}

.sidebar-nav { display: flex; flex-direction: column; gap: 2px; flex: 1; position: relative; }

.sidebar-nav a {
  padding: 11px 14px; border-radius: 10px; color: #94a3b8;
  font-size: 14px; font-weight: 500; transition: all .25s;
  display: flex; align-items: center; gap: 10px;
}
.sidebar-nav a:hover { background: rgba(99,102,241,.12); color: #c7d2fe; }

.sidebar-nav a.active {
  background: linear-gradient(135deg, rgba(99,102,241,.25), rgba(139,92,246,.15));
  color: #fff; box-shadow: 0 0 24px rgba(99,102,241,.15);
}

.nav-dot {
  width: 6px; height: 6px; border-radius: 50%; background: currentColor; opacity: .4;
}
.sidebar-nav a.active .nav-dot {
  background: var(--accent); opacity: 1; box-shadow: 0 0 8px var(--accent);
}

.sidebar-footer {
  font-size: 12px; color: #64748b;
  border-top: 1px solid rgba(99,102,241,.12); padding-top: 18px; position: relative;
}
.admin-email { margin-bottom: 8px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.logout-btn {
  width: 100%; padding: 8px; border-radius: 8px; font-size: 13px;
  background: rgba(99,102,241,.1); color: #94a3b8;
  border: 1px solid rgba(99,102,241,.15); cursor: pointer; transition: all .25s;
  font-family: inherit;
}
.logout-btn:hover { background: rgba(239,68,68,.12); color: #fca5a5; border-color: rgba(239,68,68,.2); }

.main-content { margin-left: 240px; flex: 1; padding: 32px; background: #f1f5f9; min-height: 100vh; }
</style>
