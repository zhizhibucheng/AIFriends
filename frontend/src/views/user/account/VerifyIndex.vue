<script setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {useUserStore} from '@/stores/user.js'
import api from '@/js/http/api.js'

const realName = ref('')
const idCardNumber = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const router = useRouter()
const userStore = useUserStore()

const submitVerify = async () => {
  errorMessage.value = ''

  if (!realName.value.trim() || !idCardNumber.value.trim()) {
    errorMessage.value = '姓名和身份证号不能为空'
    return
  }
  if (!/^\d{17}[\dXx]$/.test(idCardNumber.value)) {
    errorMessage.value = '身份证号格式不正确'
    return
  }

  isLoading.value = true
  try {
    const response = await api.post('/api/user/account/verify/', {
      real_name: realName.value,
      id_card_number: idCardNumber.value
    })

    if (response.data.result === 'success') {
      userStore.setVerifyStatus(response.data.is_verified, response.data.is_minor)

      // 提交成功后在前端本地进行一次简单的打码展示，以防用户未刷新页面时发生状态闪烁
      userStore.realNameMasked = realName.value.length <= 2
          ? realName.value.charAt(0) + '*'
          : realName.value.charAt(0) + '*'.repeat(realName.value.length - 2) + realName.value.slice(-1)
      userStore.idCardMasked = idCardNumber.value.slice(0, 6) + '********' + idCardNumber.value.slice(-4)

      alert('实名认证成功！')
      router.push({name: 'homepage-index'})
    }
  } catch (error) {
    errorMessage.value = error.response?.data?.error || '认证失败，请稍后重试'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="flex justify-center mt-30">
    <div v-if="userStore.isVerified"
         class="fieldset bg-base-200/20 border-base-300 rounded-box w-96 border p-6 backdrop-blur-md shadow-lg text-center">
      <div class="text-4xl mb-2">🛡️</div>
      <h2 class="text-2xl font-bold text-gray-800 mb-4">已完成实名认证</h2>

      <div class="bg-base-100/50 rounded-lg p-5 mb-4 text-left border border-base-content/10">
        <p class="text-sm text-gray-600 mb-3">
          真实姓名：<span class="font-bold text-gray-800 text-base tracking-widest ml-2">{{
            userStore.realNameMasked
          }}</span>
        </p>
        <p class="text-sm text-gray-600">
          身份证号：<span class="font-bold text-gray-800 text-base tracking-widest ml-2">{{
            userStore.idCardMasked
          }}</span>
        </p>
      </div>

      <p class="text-xs text-success font-semibold mb-6 flex items-center justify-center gap-1">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"
             class="w-4 h-4">
          <path stroke-linecap="round" stroke-linejoin="round"
                d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z"/>
        </svg>
        您的身份信息已进行金融级加密保护
      </p>

      <button @click="router.push({name: 'homepage-index'})" class="btn btn-neutral w-full">返回首页</button>
    </div>

    <form v-else @submit.prevent="submitVerify"
          class="fieldset bg-base-200/20 border-base-300 rounded-box w-96 border p-6 backdrop-blur-md shadow-lg">
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