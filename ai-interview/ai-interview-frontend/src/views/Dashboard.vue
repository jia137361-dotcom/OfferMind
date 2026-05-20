<template>
  <div class="container">
    <div class="page-header">
      <div>
        <h1 class="section-title">我的面试训练</h1>
        <p class="section-subtitle">查看你的 AI 模拟面试进度与评估结果</p>
      </div>
      <router-link to="/resume/upload" class="btn-primary">+ 开始新面试</router-link>
    </div>

    <!-- Stats cards -->
    <div v-if="!loading && interviews.length > 0" class="stats-row">
      <div class="stat-card">
        <span>全部面试</span>
        <strong>{{ interviews.length }}</strong>
      </div>
      <div class="stat-card">
        <span>进行中</span>
        <strong>{{ interviews.filter(i => i.status === 'in_progress').length }}</strong>
      </div>
      <div class="stat-card">
        <span>已完成</span>
        <strong>{{ interviews.filter(i => i.status === 'completed').length }}</strong>
      </div>
    </div>

    <div v-if="loading" class="empty-state">
      <div class="skeleton" style="width:100%;height:120px;margin-bottom:12px"></div>
      <div class="skeleton" style="width:100%;height:120px"></div>
    </div>

    <div v-else-if="interviews.length === 0" class="empty-state card">
      <div class="icon">🎯</div>
      <div class="title">还没有面试记录</div>
      <div class="desc">上传简历开始你的第一次 AI 模拟面试</div>
    </div>

    <div v-else class="interview-list">
      <div v-for="item in interviews" :key="item.interview_id" class="card interview-card">
        <div class="card-top">
          <div class="card-left">
            <div class="card-title">{{ item.target_position }}</div>
            <div class="card-meta">
              AI 模拟面试 · {{ difficultyMap[item.difficulty] || item.difficulty }}难度 · {{ item.total_questions }} 道题
            </div>
            <div class="card-date">创建时间：{{ formatDate(item.created_at) }}</div>
          </div>
          <div class="card-right">
            <span :class="item.status === 'completed' ? 'status-done' : 'status-running'">
              {{ item.status === 'completed' ? '已完成' : '进行中' }}
            </span>
            <span v-if="item.overall_score" class="card-score">{{ item.overall_score }} 分</span>
          </div>
        </div>
        <div class="card-actions">
          <router-link v-if="item.status === 'in_progress'" :to="`/interview/${item.interview_id}`" class="btn-primary btn-sm">
            继续面试
          </router-link>
          <router-link v-else :to="`/interview/${item.interview_id}/report`" class="btn-secondary btn-sm">
            查看报告
          </router-link>
          <button class="btn-danger btn-sm" @click="handleDelete(item.interview_id)">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getInterviews, deleteInterview } from '../api/interview'

const interviews = ref([])
const loading = ref(true)
const difficultyMap = { easy: '简单', medium: '中等', hard: '困难' }

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
.page-header {
  display: flex; justify-content: space-between; align-items: flex-start;
  margin-bottom: 24px;
}

/* Stats */
.stats-row {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px;
  margin-bottom: 22px;
}
.stat-card {
  padding: 20px; border-radius: 20px;
  background: #FFFFFF; border: 1px solid var(--border);
  box-shadow: 0 16px 40px rgba(15,23,42,0.06);
}
.stat-card span { font-size: 13px; color: var(--text-secondary); }
.stat-card strong { display: block; margin-top: 8px; font-size: 28px; color: var(--text); font-weight: 800; }

/* Interview cards */
.interview-list { display: flex; flex-direction: column; gap: 14px; }
.interview-card { padding: 24px; border-radius: 22px; }
.interview-card:hover { transform: translateY(-2px); box-shadow: 0 24px 60px rgba(15,23,42,0.10); }

.card-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; }
.card-left { flex: 1; }
.card-title { font-size: 18px; font-weight: 800; color: var(--text); margin-bottom: 6px; }
.card-meta { font-size: 13px; color: var(--text-secondary); }
.card-date { font-size: 12px; color: var(--text-muted); margin-top: 4px; }
.card-right { display: flex; align-items: center; gap: 12px; flex-shrink: 0; }
.card-score { font-size: 15px; font-weight: 700; color: var(--primary); }

.card-actions { display: flex; gap: 8px; }
</style>
