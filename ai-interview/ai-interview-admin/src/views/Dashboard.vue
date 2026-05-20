<template>
  <div>
    <div style="margin-bottom:28px">
      <h1 class="section-title">数据概览</h1>
      <p class="section-subtitle" style="font-size:13px;color:var(--text-muted);margin-top:4px">平台核心指标一览</p>
    </div>
    <div class="stats-grid">
      <div class="stat-card" v-for="(s, i) in statCards" :key="i">
        <div class="stat-icon">{{ s.icon }}</div>
        <div class="stat-num">{{ stats[s.key] }}</div>
        <div class="stat-label">{{ s.label }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { userApi } from '../api'

const stats = ref({ user_count: 0, resume_count: 0, interview_count: 0, completed_interview_count: 0 })

const statCards = [
  { key: 'user_count', label: '注册用户', icon: '👥' },
  { key: 'resume_count', label: '上传简历', icon: '📄' },
  { key: 'interview_count', label: '面试总数', icon: '🎤' },
  { key: 'completed_interview_count', label: '已完成面试', icon: '✅' }
]

onMounted(async () => {
  try { stats.value = await userApi.stats() } catch (e) { console.error(e) }
})
</script>

<style scoped>
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }

.stat-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 28px 24px; text-align: center;
  position: relative; overflow: hidden;
  transition: all .3s; box-shadow: var(--shadow-sm);
}
.stat-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--primary), var(--accent));
}
.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(99,102,241,.12);
}

.stat-icon { font-size: 32px; margin-bottom: 12px; }
.stat-num { font-size: 42px; font-weight: 800; color: var(--primary); letter-spacing: -1px; }
.stat-label { font-size: 13px; color: var(--text-secondary); margin-top: 6px; font-weight: 500; }
</style>
