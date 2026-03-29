<script setup>
import { ref, watch } from "vue";
import { useUserStore } from "@/stores/user.js";
import api from "@/js/http/api.js";

const props = defineProps(['voices','curVoiceId'])

const myVoice = ref(props.curVoiceId)

watch(() => props.curVoiceId, newVal => {
  myVoice.value = newVal
})

const userStore = useUserStore()

// ================= 新增：录音与语音复刻逻辑 =================
const isRecording = ref(false)
const mediaRecorder = ref(null)
const audioChunks = ref([])
const audioBlob = ref(null)
const audioUrl = ref('')

const isUploading = ref(false)
const uploadSuccessMsg = ref('')
const uploadErrorMsg = ref('')

// 开始录音
const startRecording = async () => {
  try {
    uploadSuccessMsg.value = ''
    uploadErrorMsg.value = ''
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder.value = new MediaRecorder(stream)

    mediaRecorder.value.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.value.push(event.data)
      }
    }

    mediaRecorder.value.onstop = () => {
      audioBlob.value = new Blob(audioChunks.value, { type: 'audio/webm' })
      audioUrl.value = URL.createObjectURL(audioBlob.value)
      audioChunks.value = []
      stream.getTracks().forEach(track => track.stop())
    }

    mediaRecorder.value.start()
    isRecording.value = true
  } catch (err) {
    alert('无法访问麦克风，请检查浏览器权限设置。')
    console.error(err)
  }
}

// 停止录音
const stopRecording = () => {
  if (mediaRecorder.value && mediaRecorder.value.state !== 'inactive') {
    mediaRecorder.value.stop()
    isRecording.value = false
  }
}

// 上传录音并复刻音色
const uploadVoice = async () => {
  if (!audioBlob.value) return

  isUploading.value = true
  uploadErrorMsg.value = ''
  uploadSuccessMsg.value = ''

  const formData = new FormData()
  formData.append('audio', audioBlob.value, 'custom_voice.webm')

  try {
    // 【修改点2】使用你封装好的 api 发送请求，它会自动带上正确的 BASE_URL 和 Token
    const response = await api.post('/api/create/character/voice/custom/create/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    // Axios 的返回数据在 response.data 中
    const resData = response.data

    if (resData.result === 'success') {
      uploadSuccessMsg.value = '专属音色生成成功！'
      myVoice.value = resData.voice_id
    } else {
      uploadErrorMsg.value = resData.message || '生成失败'
    }
  } catch (err) {
    console.error(err)
    // 这里可以打印更详细的后端错误信息
    uploadErrorMsg.value = err.response?.data?.message || '网络或服务器异常'
  } finally {
    isUploading.value = false
  }
}

defineExpose({
  myVoice,
})
</script>

<template>
  <fieldset class="fieldset">
    <label class="label text-base">音色</label>
    <select v-model="myVoice" class="select w-full bg-base-100/70">
      <option
          v-for="voice in voices"
          :id="voice.id"
          :value="voice.id"
      >{{voice.name}}</option>

      <option
          v-if="typeof myVoice === 'number' && !voices.find(v => v.id === myVoice)"
          :value="myVoice"
      >
        ✅ 你已绑定的专属音色
      </option>

      <option value="custom">➕ 自定义专属音色</option>
    </select>

    <div v-if="myVoice === 'custom'" class="mt-4 p-4 border border-gray-300 rounded-lg bg-gray-50">
      <p class="text-sm font-bold mb-2">🎤 录制专属音色</p>
      <p class="text-xs text-gray-500 mb-4">
        请在安静的环境下，用正常的语速和音量朗读以下文案：<br/>
        <span class="italic text-blue-600 block mt-1">“你好，我是你的专属AI助手，很高兴认识你。你可以随时和我聊天，我会尽我所能帮助你。”</span>
      </p>

      <div class="flex gap-2 mb-4">
        <button v-if="!isRecording" @click="startRecording" type="button" class="px-3 py-1 bg-blue-500 text-white text-sm rounded hover:bg-blue-600">
          开始录音
        </button>
        <button v-else @click="stopRecording" type="button" class="px-3 py-1 bg-red-500 text-white text-sm rounded hover:bg-red-600 animate-pulse">
          停止录音
        </button>
      </div>

      <div v-if="audioUrl" class="mb-4">
        <audio :src="audioUrl" controls class="w-full h-8"></audio>
      </div>

      <button v-if="audioBlob && !isUploading" @click="uploadVoice" type="button" class="w-full px-3 py-2 bg-green-500 text-white text-sm rounded hover:bg-green-600 font-bold">
        生成专属音色
      </button>

      <button v-if="isUploading" disabled type="button" class="w-full px-3 py-2 bg-gray-400 text-white text-sm rounded cursor-not-allowed">
        ⏳ 请耐心等待...
      </button>

      <p v-if="uploadSuccessMsg" class="text-xs text-green-600 mt-2 font-bold">{{ uploadSuccessMsg }}</p>
      <p v-if="uploadErrorMsg" class="text-xs text-red-600 mt-2 font-bold">{{ uploadErrorMsg }}</p>
    </div>

  </fieldset>
</template>

<style scoped>

</style>