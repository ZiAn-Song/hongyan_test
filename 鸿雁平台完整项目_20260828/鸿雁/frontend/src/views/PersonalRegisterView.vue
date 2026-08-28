<template>
  <div class="page">
    <AppHeader />
    <div class="register-container">
      <div class="form-card">
        <div class="card-header">
          <h1><i class="fas fa-user-circle"></i> 个人信息收集表</h1>
          <p class="subtitle">请准确填写您的个人信息，所有带 * 的字段为必填项</p>
        </div>

        <div class="form-body">
          <div class="instructions">
            <h3><i class="fas fa-info-circle"></i> 填写说明</h3>
            <p>请确保您填写的信息真实有效，这些信息将用于身份验证和相关联系。我们承诺保护您的个人隐私。</p>
          </div>

          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            label-position="top"
            size="large"
            @submit.prevent="handleSubmit"
          >
            <el-form-item label="个人姓名" prop="fullName">
              <el-input v-model="form.fullName" placeholder="请输入您的真实姓名" />
            </el-form-item>

            <el-form-item label="密码" prop="password">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="请输入您的密码（至少6位）"
                show-password
              />
            </el-form-item>

            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="form.gender">
                <el-radio value="男">男</el-radio>
                <el-radio value="女">女</el-radio>
                <el-radio value="其他">其他</el-radio>
              </el-radio-group>
            </el-form-item>

            <el-row :gutter="20">
              <el-col :xs="24" :sm="12">
                <el-form-item label="所属高校名称" prop="university">
                  <el-input v-model="form.university" placeholder="请输入您所在的高校名称" />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="学号" prop="studentId">
                  <el-input v-model="form.studentId" placeholder="请输入您的学号" />
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item label="联系方式" prop="contact">
              <el-input v-model="form.contact" placeholder="请输入您的手机号码" />
            </el-form-item>

            <el-form-item label="电子邮箱（可选）">
              <el-input v-model="form.email" placeholder="请输入您的邮箱地址" />
            </el-form-item>

            <el-form-item label="专业（可选）">
              <el-input v-model="form.major" placeholder="请输入您的专业" />
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                class="submit-btn"
                :loading="submitting"
                @click="handleSubmit"
              >
                <i class="fas fa-check-circle"></i> 提交信息
              </el-button>
            </el-form-item>
          </el-form>
        </div>

        <div class="card-footer">
          <p><i class="fas fa-lock"></i> 隐私保护：我们承诺严格遵守个人信息保护相关法律法规</p>
          <p class="copyright">© 2026 个人信息收集系统 | 仅用于信息登记与核实</p>
        </div>
      </div>
    </div>
    <AppFooter />
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref(null)
const submitting = ref(false)

const form = reactive({
  fullName: '',
  password: '',
  gender: '',
  university: '',
  studentId: '',
  contact: '',
  email: '',
  major: ''
})

const rules = {
  fullName: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, message: '姓名至少2个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ],
  university: [
    { required: true, message: '请输入高校名称', trigger: 'blur' }
  ],
  studentId: [
    { required: true, message: '请输入学号', trigger: 'blur' },
    { min: 5, message: '学号长度不足', trigger: 'blur' }
  ],
  contact: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的11位手机号码', trigger: 'blur' }
  ]
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitting.value = true
    try {
      await authStore.registerPersonalUser({
        student_id: form.studentId,
        full_name: form.fullName,
        password: form.password,
        gender: form.gender,
        university: form.university,
        contact: form.contact,
        email: form.email || undefined,
        major: form.major || undefined
      })

      ElMessageBox.alert(
        `姓名：${form.fullName}\n高校：${form.university}\n提交时间：${new Date().toLocaleString()}`,
        '个人信息提交成功！',
        { confirmButtonText: '去登录', type: 'success' }
      ).then(() => {
        router.push('/login')
      })
    } catch (error) {
      const msg = error.response?.data?.detail || '注册失败，请稍后重试'
      ElMessage.error(msg)
    } finally {
      submitting.value = false
    }
  })
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 20px;
  min-height: calc(100vh - var(--header-height, 90px));
  background-color: #f8fafc;
}

.form-card {
  width: 100%;
  max-width: 700px;
  background-color: var(--color-bg-card);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.card-header {
  background-color: var(--color-primary-darker);
  color: white;
  padding: 30px;
  text-align: center;
}

.card-header h1 {
  font-size: 1.8rem;
  margin-bottom: 8px;
}

.card-header h1 i {
  margin-right: 10px;
}

.subtitle {
  font-size: 1rem;
  opacity: 0.9;
  font-weight: 300;
}

.form-body {
  padding: 30px;
}

.instructions {
  background-color: rgba(239, 246, 255, 0.6);
  border-left: 4px solid var(--color-primary-darker);
  padding: 16px;
  margin-bottom: 25px;
  border-radius: 0 10px 10px 0;
}

.instructions h3 {
  margin-bottom: 8px;
  color: var(--color-accent);
  display: flex;
  align-items: center;
  font-size: 1.1rem;
}

.instructions h3 i {
  margin-right: 8px;
}

.instructions p {
  color: #475569;
  font-size: 0.95rem;
}

.submit-btn {
  width: 100%;
  background-color: var(--color-primary-darker);
  border-color: var(--color-primary-darker);
  font-size: 18px;
  padding: 18px;
  letter-spacing: 0.5px;
}

.submit-btn:hover {
  background: linear-gradient(to right, #1e3a8a, #1e293b);
  border-color: #1e3a8a;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(30, 58, 138, 0.25);
}

.card-footer {
  text-align: center;
  padding: 20px;
  color: #666;
  font-size: 0.9rem;
  border-top: 1px solid var(--color-border);
  background-color: #f9f9f9;
}

.card-footer .copyright {
  margin-top: 8px;
}

@media (max-width: 640px) {
  .card-header {
    padding: 25px 20px;
  }

  .card-header h1 {
    font-size: 1.5rem;
  }

  .form-body {
    padding: 25px;
  }

  .register-container {
    padding: 15px;
  }
}
</style>
