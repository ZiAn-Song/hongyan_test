<template>
  <div class="page">
    <AppHeader />

    <section class="page-header">
      <div class="container">
        <h1><i class="fas fa-comments"></i> 对接中心</h1>
        <p>平台内直接沟通——对接意向、洽谈记录都在这里</p>
      </div>
    </section>

    <div class="container content-area">
      <div v-if="!authStore.isLoggedIn" class="login-gate">
        <i class="fas fa-lock"></i>
        <p>登录后查看你的对接会话</p>
        <router-link to="/login" class="gate-btn">去登录</router-link>
      </div>

      <div v-else class="cc-layout">
        <!-- 左：会话列表 -->
        <aside class="thread-list">
          <div v-if="loading" class="loading"><div class="spinner"></div><p>加载中...</p></div>
          <div v-else-if="threads.length === 0" class="empty">
            <i class="fas fa-inbox"></i>
            <p>暂无对接会话</p>
            <p class="empty-sub">在「需求大厅」匹配结果里点「发起对接」开始沟通</p>
          </div>
          <button
            v-for="t in threads"
            :key="t.id"
            class="thread-item"
            :class="{ active: activeId === t.id }"
            @click="openThread(t.id)"
          >
            <span class="t-dot" v-if="t.unread > 0"></span>
            <div class="t-main">
              <p class="t-title">
                <span class="t-tag" :class="t.subject_type">{{ subjectLabel(t.subject_type) }}</span>
                {{ truncate(t.subject_title, 26) }}
              </p>
              <p class="t-preview">{{ truncate(t.last_message, 32) }}</p>
            </div>
            <span class="t-unread" v-if="t.unread > 0">{{ t.unread }}</span>
          </button>
        </aside>

        <!-- 右：聊天窗 -->
        <section class="chat-pane" v-if="active">
          <header class="chat-head">
            <div>
              <h3 class="ch-title">{{ truncate(active.subject_title, 34) }}</h3>
              <p class="ch-meta">
                {{ subjectLabel(active.subject_type) }} · 发起人 {{ active.initiator_name || '我' }}
              </p>
            </div>
            <a v-if="active.entity_link" :href="active.entity_link" target="_blank" rel="noopener" class="ch-link">
              <i class="fas fa-external-link-alt"></i> 信源原文
            </a>
          </header>

          <div class="ch-contact" v-if="active.entity_contact">
            <i class="fas fa-address-card"></i>
            <span><b>官方渠道</b>{{ active.entity_contact }}</span>
          </div>

          <div class="chat-msgs" ref="msgsBox">
            <div v-for="msg in messages" :key="msg.id" class="msg-row" :class="{ mine: msg.mine }">
              <div class="msg-bubble">
                <p class="msg-content">{{ msg.content }}</p>
                <p class="msg-time">{{ shortTime(msg.created_at) }} · {{ msg.sender_name || '用户' }}</p>
              </div>
            </div>
            <div v-if="messages.length === 0" class="chat-empty">还没有消息</div>
          </div>

          <footer class="chat-input">
            <textarea v-model="reply" rows="2" placeholder="输入回复...（Enter 发送，Shift+Enter 换行）"
              @keydown.enter.exact.prevent="send"></textarea>
            <button :disabled="sending || !reply.trim()" @click="send">
              <i class="fas" :class="sending ? 'fa-spinner fa-spin' : 'fa-paper-plane'"></i> 发送
            </button>
          </footer>
        </section>

        <section class="chat-pane chat-placeholder" v-else>
          <i class="fas fa-comments"></i>
          <p>选择左侧会话开始沟通</p>
        </section>
      </div>
    </div>

    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { listThreads, getThreadMessages, sendThreadMessage } from '@/api/contact'

const authStore = useAuthStore()
const threads = ref([])
const activeId = ref(null)
const active = ref(null)
const messages = ref([])
const loading = ref(false)
const reply = ref('')
const sending = ref(false)
const msgsBox = ref(null)
let pollTimer = null

const subjectLabel = (t) => ({ demand: '边疆需求', supply: '企业/机构', talent: '山大人才' }[t] || t)
const truncate = (s, n) => (s || '').length > n ? (s || '').slice(0, n) + '…' : (s || '')
const shortTime = (iso) => (iso || '').replace('T', ' ').slice(5, 16)

const loadThreads = async () => {
  loading.value = !threads.value.length
  try {
    const res = await listThreads()
    threads.value = res.items || []
  } catch (e) { console.error(e) }
  loading.value = false
}

const openThread = async (id) => {
  activeId.value = id
  try {
    const res = await getThreadMessages(id)
    active.value = res.thread
    messages.value = res.items
    await nextTick()
    if (msgsBox.value) msgsBox.value.scrollTop = msgsBox.value.scrollHeight
    loadThreads()   // 拉取后未读清零，刷新角标
  } catch (e) { console.error(e) }
}

const send = async () => {
  if (!reply.value.trim() || sending.value || !activeId.value) return
  sending.value = true
  try {
    await sendThreadMessage(activeId.value, reply.value.trim())
    reply.value = ''
    await openThread(activeId.value)
  } catch (e) { console.error(e) }
  sending.value = false
}

onMounted(async () => {
  if (authStore.isLoggedIn) {
    await loadThreads()
    if (threads.value.length) openThread(threads.value[0].id)
    pollTimer = setInterval(async () => {          // 轻量轮询：6 秒
      if (activeId.value) await openThread(activeId.value)
      else await loadThreads()
    }, 6000)
  }
})
onUnmounted(() => { if (pollTimer) clearInterval(pollTimer) })
</script>

<style scoped>
.page { min-height: 100vh; background: var(--paper); }

.page-header {
  background: var(--paper-2);
  color: var(--ink);
  padding: 44px 4% 34px;
  text-align: center;
  border-bottom: 3px double var(--ink);
}
.page-header h1 { font-size: 1.9rem; letter-spacing: 2px; }
.page-header p { font-size: 0.95rem; color: var(--ink-3); margin-top: 8px; }

.content-area { padding: 30px 4% 60px; }

.login-gate {
  text-align: center; padding: 70px 0; color: var(--ink-3);
}
.login-gate i { font-size: 34px; margin-bottom: 14px; }
.gate-btn {
  display: inline-block; margin-top: 14px; padding: 9px 30px;
  background: var(--color-primary); color: #fff; border-radius: var(--radius-sm);
  font-weight: 650; letter-spacing: 1px;
}

.cc-layout {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 20px;
  max-width: var(--max-width);
  margin: 0 auto;
  min-height: 540px;
}

/* 左：会话列表 */
.thread-list {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow-y: auto;
  max-height: 640px;
}
.thread-item {
  width: 100%; text-align: left;
  display: flex; align-items: center; gap: 10px;
  padding: 14px 16px;
  background: none; border: none; border-bottom: 1px solid var(--color-border);
  cursor: pointer; position: relative;
  transition: background 0.2s;
}
.thread-item:hover { background: var(--paper-2); }
.thread-item.active { background: var(--color-primary-light); border-left: 3px solid var(--color-primary); }
.t-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--color-accent); position: absolute; left: 6px; top: 18px;
}
.t-main { flex: 1; min-width: 0; }
.t-title { font-size: 13.5px; font-weight: 650; color: var(--ink); display: flex; align-items: center; gap: 7px; }
.t-tag {
  font-size: 10px; letter-spacing: 1px; padding: 1px 7px;
  border: 1px solid; border-radius: 2px; white-space: nowrap; font-weight: 600;
}
.t-tag.demand { color: var(--color-accent); border-color: rgba(163,58,42,.4); }
.t-tag.supply { color: var(--color-primary); border-color: rgba(30,58,110,.35); }
.t-tag.talent { color: var(--talent); border-color: rgba(109,76,159,.4); }
.t-preview { font-size: 12px; color: var(--ink-3); margin-top: 4px; }
.t-unread {
  min-width: 19px; height: 19px; border-radius: 99px;
  background: var(--color-accent); color: #fff;
  font-size: 11px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.empty, .loading { text-align: center; padding: 60px 16px; color: var(--ink-3); }
.empty i { font-size: 30px; margin-bottom: 12px; }
.empty-sub { font-size: 12px; margin-top: 6px; }

/* 右：聊天窗 */
.chat-pane {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  display: flex; flex-direction: column;
  max-height: 640px;
}
.chat-placeholder { align-items: center; justify-content: center; color: var(--ink-3); }
.chat-placeholder i { font-size: 34px; margin-bottom: 12px; }

.chat-head {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 18px;
  border-bottom: 1px solid var(--color-border);
}
.ch-title { font-family: var(--font-serif); font-size: 15px; color: var(--ink); }
.ch-meta { font-size: 11.5px; color: var(--ink-3); margin-top: 3px; }
.ch-link { font-size: 12px; color: var(--color-primary); text-decoration: none; white-space: nowrap; }

.ch-contact {
  display: flex; gap: 9px; align-items: flex-start;
  margin: 12px 18px 0; padding: 8px 12px;
  background: var(--paper-2);
  border-left: 2px solid var(--el-color-success);
  border-radius: 0 4px 4px 0;
  font-size: 12.5px; color: var(--ink-2); line-height: 1.6;
}
.ch-contact i { color: var(--el-color-success); margin-top: 3px; }
.ch-contact b { color: var(--el-color-success); margin-right: 7px; }

.chat-msgs { flex: 1; overflow-y: auto; padding: 16px 18px; }
.msg-row { display: flex; margin-bottom: 12px; }
.msg-row.mine { justify-content: flex-end; }
.msg-bubble {
  max-width: 78%;
  padding: 9px 13px;
  border-radius: var(--radius-md);
  background: var(--paper-2);
  border: 1px solid var(--color-border);
}
.msg-row.mine .msg-bubble {
  background: var(--color-primary-light);
  border-color: rgba(30, 58, 110, 0.25);
}
.msg-content { font-size: 13.5px; line-height: 1.7; color: var(--ink); white-space: pre-wrap; word-break: break-all; }
.msg-time { font-size: 10.5px; color: var(--ink-3); margin-top: 5px; text-align: right; }
.chat-empty { text-align: center; color: var(--ink-3); font-size: 12.5px; padding: 30px 0; }

.chat-input {
  display: flex; gap: 10px; align-items: flex-end;
  padding: 13px 18px;
  border-top: 1px solid var(--color-border);
}
.chat-input textarea {
  flex: 1; resize: none;
  padding: 9px 12px;
  font-size: 13px; line-height: 1.6;
  color: var(--ink);
  background: var(--paper);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: var(--font-family);
}
.chat-input textarea:focus { outline: none; border-color: var(--color-primary); }
.chat-input button {
  padding: 9px 20px;
  background: var(--color-primary); color: #fff;
  border: none; border-radius: var(--radius-sm);
  font-size: 13px; font-weight: 650; letter-spacing: 1px; cursor: pointer;
  transition: transform 0.25s var(--ease-out), background 0.2s;
}
.chat-input button:hover:not(:disabled) { background: var(--color-primary-dark); transform: translateY(-1px); }
.chat-input button:disabled { opacity: 0.45; cursor: not-allowed; }

@media (max-width: 860px) {
  .cc-layout { grid-template-columns: 1fr; }
  .thread-list { max-height: 260px; }
}
</style>
