<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user.js'
import api from '@/js/http/api.js'

const realName = ref('')
const idCardNumber = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const router = useRouter()
const userStore = useUserStore()

const submitVerify = async () => {
  errorMessage.value = ''

  // 1. 前端初步非空拦截
  if (!realName.value.trim() || !idCardNumber.value.trim()) {
    errorMessage.value = '姓名和身份证号不能为空'
    return
  }
  // 2. 身份证号正则拦截 (18位，末尾可为X)
  if (!/^\d{17}[\dXx]$/.test(idCardNumber.value)) {
    errorMessage.value = '身份证号格式不正确'
    return
  }

  isLoading.value = true
  try {
    // 调用后端认证接口
    const response = await api.post('/api/user/account/verify/', {
      real_name: realName.value,
      id_card_number: idCardNumber.value
    })

    if (response.data.result === 'success') {
      // 认证成功：更新 Store 状态
      userStore.setVerifyStatus(response.data.is_verified, response.data.is_minor)
      alert('实名认证成功！')

      // 认证完成后跳转回首页
      router.push({ name: 'homepage-index' })
    }
  } catch (error) {
    // 捕获并显示后端返回的错误信息
    errorMessage.value = error.response?.data?.error || '认证失败，请稍后重试'
  } finally {
    isLoading.value = false
  }
}
</script>


<template>
  <div class="flex justify-center mt-30">

    <form @submit.prevent="submitVerify" class="fieldset bg-base-200/20 border-base-300 rounded-box w-96 border p-6 backdrop-blur-md shadow-lg">

      <h2 class="text-2xl font-bold text-center text-gray-800 mb-2">实名认证</h2>
      <p class="text-xs text-gray-600 mb-6 leading-relaxed">
        根据《人工智能拟人化互动服务管理暂行办法》规定，使用本系统的情感互动功能必须先进行实名认证。
      </p>

      <label class="label">
        <span class="label-text text-base text-gray-700 font-bold">真实姓名</span>
      </label>
      <input
        type="text"
        v-model="realName"
        class="input input-bordered bg-base-100/70 text-base-content placeholder-gray-400 w-full"
        placeholder="请输入您的真实姓名"
      />

      <label class="label mt-2">
        <span class="label-text text-base text-gray-700 font-bold">身份证号</span>
      </label>
      <input
        type="text"
        v-model="idCardNumber"
        class="input input-bordered bg-base-100/70 text-base-content placeholder-gray-400 w-full"
        placeholder="请输入18位身份证号"
        maxlength="18"
      />

      <p v-if="errorMessage" class="text-sm text-red-500 mt-2">{{ errorMessage }}</p>

      <button
        class="btn btn-neutral mt-6 w-full"
        type="submit"
        :disabled="isLoading"
      >
        <span v-if="isLoading" class="loading loading-spinner"></span>
        {{ isLoading ? '认证中...' : '提交认证' }}
      </button>

    </form>
  </div>
</template>


<style scoped>

</style>