<template>
  <div class="page">
    <AppHeader />
    <div class="register-container">
      <div class="form-card">
        <div class="card-header">
          <h1><i class="fas fa-landmark"></i> 政企信息收集表</h1>
          <p class="subtitle">请准确填写政府或企业的基本信息，所有带 * 的字段为必填项</p>
        </div>

        <div class="form-body">
          <div class="instructions">
            <h3><i class="fas fa-info-circle"></i> 填写说明</h3>
            <p>本表单用于收集政府机构或企业单位的基本信息。请确保填写的信息真实有效，我们将严格遵守信息保密规定，仅用于信息备案和联系使用。</p>
          </div>

          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            label-position="top"
            size="large"
          >
            <el-form-item label="机构类型" prop="orgType">
              <el-radio-group v-model="form.orgType">
                <el-radio value="政府机构">政府机构</el-radio>
                <el-radio value="企业单位">企业单位</el-radio>
                <el-radio value="事业单位">事业单位</el-radio>
                <el-radio value="社会组织">社会组织</el-radio>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="政府/企业名称" prop="orgName">
              <el-input v-model="form.orgName" placeholder="请输入完整的机构名称">
                <template #suffix><i class="fas fa-building" style="color: #94a3b8"></i></template>
              </el-input>
            </el-form-item>

            <el-row :gutter="20">
              <el-col :xs="24" :sm="12">
                <el-form-item label="行政地点" prop="adminLocation">
                  <el-input v-model="form.adminLocation" placeholder="省/市/区/详细地址">
                    <template #suffix><i class="fas fa-map-marker-alt" style="color: #94a3b8"></i></template>
                  </el-input>
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="行政编码" prop="adminCode">
                  <el-input
                    v-model="form.adminCode"
                    placeholder="6位行政区域编码"
                    maxlength="6"
                    @input="form.adminCode = form.adminCode.replace(/\D/g, '')"
                  >
                    <template #suffix><i class="fas fa-hashtag" style="color: #94a3b8"></i></template>
                  </el-input>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :xs="24" :sm="12">
                <el-form-item label="政府/企业邮箱" prop="orgEmail">
                  <el-input v-model="form.orgEmail" placeholder="请输入机构官方邮箱">
                    <template #suffix><i class="fas fa-envelope" style="color: #94a3b8"></i></template>
                  </el-input>
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="负责人姓名" prop="contactPerson">
                  <el-input v-model="form.contactPerson" placeholder="请输入负责人姓名">
                    <template #suffix><i class="fas fa-user" style="color: #94a3b8"></i></template>
                  </el-input>
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item label="负责人联系方式" prop="contactPhone">
              <el-input v-model="form.contactPhone" placeholder="请输入负责人手机号码">
                <template #suffix><i class="fas fa-phone" style="color: #94a3b8"></i></template>
              </el-input>
            </el-form-item>

            <el-form-item label="登录密码" prop="password">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="请设置登录密码（至少6位）"
                show-password
              >
                <template #suffix><i class="fas fa-lock" style="color: #94a3b8"></i></template>
              </el-input>
            </el-form-item>

            <el-form-item label="政府/企业简介" prop="orgIntroduction">
              <el-input
                v-model="form.orgIntroduction"
                type="textarea"
                :rows="6"
                placeholder="请简要介绍机构的基本情况、主要职能或业务范围、规模等（建议200-800字）"
                maxlength="800"
                show-word-limit
              />
            </el-form-item>

            <el-form-item label="补充信息（可选）">
              <el-input
                v-model="form.additionalInfo"
                type="textarea"
                :rows="4"
                placeholder="可填写其他需要说明的信息，如特殊要求、备注等"
                maxlength="500"
                show-word-limit
              />
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                class="submit-btn"
                :loading="submitting"
                @click="handleSubmit"
              >
                <i class="fas fa-paper-plane"></i> 提交信息
              </el-button>
            </el-form-item>
          </el-form>
        </div>

        <div class="card-footer">
          <p><i class="fas fa-shield-alt"></i> 信息安全承诺：我们承诺严格遵守《中华人民共和国网络安全法》及相关法律法规，确保信息安全</p>
          <p class="copyright">© 2026 政企信息管理系统 | 服务热线：400-xxx-xxxx</p>
        </div>
      </div>
    </div>

    <el-dialog v-model="showSuccess" title="" width="400" center :show-close="false">
      <div class="success-modal-content">
        <div class="success-icon"><i class="fas fa-check-circle"></i></div>
        <h2>信息提交成功！</h2>
        <p>您的政企信息已成功提交至系统，信息编号为：<strong>{{ infoNumber }}</strong></p>
        <p class="modal-hint">我们的工作人员将在3个工作日内进行审核，审核结果将发送至您填写的邮箱。</p>
      </div>
      <template #footer>
        <el-button type="primary" @click="closeSuccessModal">确定</el-button>
      </template>
    </el-dialog>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref(null)
const submitting = ref(false)
const showSuccess = ref(false)
const infoNumber = ref('')

const form = reactive({
  orgType: '政府机构',
  orgName: '',
  adminLocation: '',
  adminCode: '',
  orgEmail: '',
  contactPerson: '',
  contactPhone: '',
  password: '',
  orgIntroduction: '',
  additionalInfo: ''
})

const rules = {
  orgType: [{ required: true, message: '请选择机构类型', trigger: 'change' }],
  orgName: [
    { required: true, message: '请输入机构名称', trigger: 'blur' },
    { min: 2, message: '机构名称过短', trigger: 'blur' }
  ],
  adminLocation: [
    { required: true, message: '请输入行政地点', trigger: 'blur' },
    { min: 5, message: '地址过短，请填写详细地址', trigger: 'blur' }
  ],
  adminCode: [
    { required: true, message: '请输入行政编码', trigger: 'blur' },
    { len: 6, message: '行政编码必须为6位数字', trigger: 'blur' }
  ],
  orgEmail: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
  ],
  contactPerson: [
    { required: true, message: '请输入负责人姓名', trigger: 'blur' },
    { pattern: /^[\u4e00-\u9fa5]{2,10}$/, message: '请输入有效的中文姓名', trigger: 'blur' }
  ],
  contactPhone: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的11位手机号码', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请设置密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  orgIntroduction: [
    { required: true, message: '请输入机构简介', trigger: 'blur' },
    { min: 50, message: '简介过短，建议不少于50字', trigger: 'blur' }
  ]
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitting.value = true
    try {
      const number = 'GE' + new Date().getTime().toString().slice(-8)
      infoNumber.value = number

      await authStore.registerEnterpriseUser({
        org_name: form.orgName,
        org_type: form.orgType,
        admin_location: form.adminLocation,
        admin_code: form.adminCode,
        org_email: form.orgEmail,
        contact_person: form.contactPerson,
        contact_phone: form.contactPhone,
        password: form.password,
        org_profile: form.orgIntroduction,
        additional_info: form.additionalInfo || undefined
      })

      showSuccess.value = true
    } catch (error) {
      const msg = error.response?.data?.detail || '注册失败，请稍后重试'
      ElMessage.error(msg)
    } finally {
      submitting.value = false
    }
  })
}

const closeSuccessModal = () => {
  showSuccess.value = false
  formRef.value?.resetFields()
  router.push('/login')
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 20px;
  min-height: calc(100vh - var(--header-height, 90px));
  background-color: var(--color-bg-alt);
}

.form-card {
  width: 100%;
  max-width: 800px;
  background-color: var(--color-bg-card);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.card-header {
  background-color: var(--color-primary-darker);
  color: white;
  padding: 35px 30px;
  text-align: center;
}

.card-header h1 {
  font-size: 2rem;
  margin-bottom: 10px;
}

.card-header h1 i {
  margin-right: 10px;
}

.subtitle {
  font-size: 1.05rem;
  opacity: 0.9;
  font-weight: 300;
  max-width: 600px;
  margin: 0 auto;
}

.form-body {
  padding: 35px;
}

.instructions {
  background-color: rgba(241, 245, 249, 0.7);
  border-left: 4px solid var(--color-primary-darker);
  padding: 18px;
  margin-bottom: 30px;
  border-radius: 0 10px 10px 0;
}

.instructions h3 {
  margin-bottom: 10px;
  color: #1e3a8a;
  display: flex;
  align-items: center;
  font-size: 1.15rem;
}

.instructions h3 i {
  margin-right: 8px;
}

.instructions p {
  color: #475569;
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
  background: linear-gradient(to right, #1e293b, #0f172a);
  border-color: #1e293b;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(30, 58, 138, 0.25);
}

.card-footer {
  text-align: center;
  padding: 25px;
  color: #64748b;
  font-size: 0.95rem;
  border-top: 1px solid #e2e8f0;
  background-color: #f8fafc;
}

.card-footer .copyright {
  margin-top: 8px;
}

.success-modal-content {
  text-align: center;
}

.success-icon {
  color: var(--el-color-success);
  font-size: 3.5rem;
  margin-bottom: 15px;
}

.success-modal-content h2 {
  color: #1e293b;
  margin-bottom: 15px;
}

.success-modal-content p {
  margin-bottom: 10px;
  font-size: 16px;
  line-height: 1.6;
  color: #475569;
}

.modal-hint {
  font-size: 14px !important;
  color: #94a3b8 !important;
}

@media (max-width: 768px) {
  .card-header {
    padding: 25px 20px;
  }

  .card-header h1 {
    font-size: 1.6rem;
  }

  .form-body {
    padding: 25px;
  }

  .register-container {
    padding: 10px;
  }
}
</style>
