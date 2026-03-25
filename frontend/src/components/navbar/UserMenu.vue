<script setup>
import {useUserStore} from "@/stores/user.js";
import UserSpaceIndex from "@/components/navbar/icons/UserSpaceIndex.vue";
import ProfileIndex from "@/views/user/profile/ProfileIndex.vue";
import UserProfileIcon from "@/components/navbar/icons/UserProfileIcon.vue";
import UserLogoutIcon from "@/components/navbar/icons/UserLogoutIcon.vue";
import {useRouter} from "vue-router";
import api from "@/js/http/api.js";
import { ref } from "vue";

const user =useUserStore()
const router = useRouter()
const fileInputRef = ref(null)

function closeMenu() {
  const element = document.activeElement
  if (element && element instanceof HTMLElement) element.blur()
}

async function handleLogout() {
  try{
    const res = await api.post('/api/user/account/logout/')
    if(res.data.result === 'success'){
      user.logout()
      await router.push({
        name: 'homepage-index'
      })
    }
  }catch(error){
    user.logout()
     await router.push({
        name: 'homepage-index'
     })
  }
}

// 新增：点击“设置背景”时触发隐藏的文件选择器
function triggerFileInput() {
  if (fileInputRef.value) {
    fileInputRef.value.click()
  }
  closeMenu() // 收起下拉菜单
}

// 新增：处理选中图片后的上传逻辑
async function handleBackgroundUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  // 类型校验：只允许图片
  if (!file.type.startsWith('image/')) {
    alert('请选择有效的图片文件！')
    return
  }

  // 构造上传的 FormData，键名必须与后端 update 接口里的保持一致
  const formData = new FormData()
  formData.append('app_background', file)

  try {
    const res = await api.post('/api/user/profile/update/', formData)
    const data = res.data
    if (data.result === 'success') {
      // 上传成功！立刻将后端返回的新背景 URL 存入 Pinia Store
      // （因为我们在第五步会把 App.vue 绑定到这个变量上，所以只要这里一改，背景瞬间就会变换）
      user.setAppBackground(data.app_background)
    } else {
      alert('背景更新失败: ' + data.result)
    }
  } catch (err) {
    alert('系统异常，图片上传失败')
  } finally {
    // 清空 input 值，保证下次选择同一张图片时也能触发 change 事件
    event.target.value = ''
  }
}

async function handleRestoreBackground() {
  // 构造带有清除信号的表单数据
  const formData = new FormData()
  formData.append('clear_app_background', 'true')

  try {
    const res = await api.post('/api/user/profile/update/', formData)
    if (res.data.result === 'success') {
      // 后端清除成功后，前端立刻切回本地默认图
      user.restoreDefaultBackground()
    } else {
      alert('恢复默认背景失败: ' + res.data.result)
    }
  } catch (err) {
    alert('系统异常，恢复失败')
  }
  closeMenu() // 收起下拉菜单
}
</script>

<template>
  <div class="dropdown dropdown-end">
    <div tabindex="0" role="button" class="avatar btn btn-circle w-8 h-8 mr-6">
      <div class="w-8 rounded-full">
        <img :src="user.photo" alt="">
      </div>

    </div>
    <ul tabindex="-1" class="dropdown-content menu bg-base-100 rounded-box z-1 w-48 p-2 shadow-lg">
      <li>
        <RouterLink @click="closeMenu" :to="{name:'user-space-index',params:{user_id:user.id}}">
          <div class="avatar">
            <div class="w-10 rounded-full">
              <img :src="user.photo" alt="">
            </div>
          </div>
          <span class="text-base font-bold line-clamp-1 break-all">{{user.username}}</span>
        </RouterLink>
      </li>
      <li>
        <RouterLink @click="closeMenu" :to="{name:'user-space-index',params:{user_id:user.id}}" class="text-sm font-bold py-3">
          <UserSpaceIndex />
          个人空间
        </RouterLink>
      </li>
      <li>
        <RouterLink @click="closeMenu" :to="{name:'user-profile-index'}" class="text-sm font-bold py-3">
          <UserProfileIcon />
          编辑资料
        </RouterLink>
      </li>

      <li>
        <a @click="triggerFileInput" class="text-sm font-bold py-3">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
          </svg>
          设置背景
        </a>
      </li>

      <li>
        <a @click="handleRestoreBackground" class="text-sm font-bold py-3">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 15L3 9m0 0l6-6M3 9h12a6 6 0 010 12h-3" />
          </svg>
          恢复默认背景
        </a>
      </li>

      <div class="divider my-0"></div> <li>
        <a @click="handleLogout" class="text-sm font-bold py-3">
          <UserLogoutIcon />
          退出登录
        </a>
      </li>
    </ul>

    <input
      type="file"
      ref="fileInputRef"
      @change="handleBackgroundUpload"
      accept="image/*"
      class="hidden"
    />
  </div>
</template>

<style scoped>

</style>