<script setup>
import {onBeforeUnmount, ref, useTemplateRef} from "vue";
import {useUserStore} from "@/stores/user.js";
import UpdateCharacter from "@/views/create/character/UpdateCharacter.vue";
import UpdateIcon from "@/components/character/icons/UpdateIcon.vue";
import RemoveIcon from "@/components/character/icons/RemoveIcon.vue";
import api from "@/js/http/api.js";
import ChatField from "@/components/character/chat_field/ChatField.vue";
import {useRouter} from "vue-router";

const props = defineProps(['character','canEdit','canRemoveFriend','friendId'])
const emit = defineEmits(["remove"]);
const isHover = ref(false)
const user = useUserStore()
const router = useRouter()

const showErrorToast = ref(false)
const errorMessage = ref("该角色已转为私密状态不可见，请刷新")
const countdown = ref(5) // 新增：倒计时秒数
let refreshTimer = null  // 新增：保存定时器实例

function doRefresh() {
  if (refreshTimer) {
    clearInterval(refreshTimer) // 清除定时器
  }
  window.location.reload()
}

async function handleRemoveCharacter(){
  try{
    const res = await api.post('/api/create/character/remove/',{
      character_id:props.character.id,
    })
    if(res.data.result === 'success'){
      emit('remove',props.character.id)
    }
  }catch(err){
  }
}

async function handleRemoveFriend(){
  try{
    const res = await api.post('/api/friend/remove/',{
      friend_id:props.friendId,
    })
    if(res.data.result === 'success'){
      emit('remove',props.friendId)
    }
  }catch(err){
  }
}

const chatFieldRef = useTemplateRef('chat-field-ref')
const friend = ref(null)

async function openChatField(){
  if(!user.isLogin()){
    await router.push({
      name: 'user-account-login-index',
    })
    return
  }
  if (!user.isVerified) {
    router.push({ name: 'user-verify-index' })
    return
  }
  if (user.isMinor) {
    alert('根据《人工智能拟人化互动服务管理暂行办法》规定，未成年人无法使用AI聊天服务。')
  }else {
    try{
      const res = await api.post('/api/friend/get_or_create/',{
        character_id:props.character.id,
      })
      const data= res.data
      if(data.result === 'success'){
        friend.value=data.friend
        chatFieldRef.value.showModal()
      }
    }catch(err){
      if (err.response && err.response.status === 403) {
        if (err.response.data && err.response.data.result) {
          errorMessage.value = err.response.data.result
        }
        showErrorToast.value = true
        countdown.value = 5 // 重置倒计时

        // 如果已经有定时器，先清除
        if (refreshTimer) clearInterval(refreshTimer)
        // 开启每秒递减的定时器
        refreshTimer = setInterval(() => {
          countdown.value--
          if (countdown.value <= 0) {
            clearInterval(refreshTimer)
            if (showErrorToast.value) { // 确认提示框没被提前关闭
               doRefresh()
            }
          }
        }, 1000)
      }
    }
  }
}

// 组件卸载时清理定时器，防止内存泄漏
onBeforeUnmount(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})

</script>

<template>
 <div>

   <div v-if="showErrorToast" class="toast toast-top toast-center z-[100]">
     <div class="alert alert-error cursor-pointer shadow-lg" @click="doRefresh">
       <span>{{ errorMessage }}({{ countdown }}秒后自动刷新)</span>
     </div>
   </div>

   <div class="avatar cursor-pointer" @mouseover="isHover = true" @mouseout="isHover = false" @click="openChatField">
     <div class="w-60 h-100 rounded-2xl relative">
       <img :src="character.background_image" class="transition-transform duration-300"  :class="{'scale-120':isHover}" alt="" >
       <div class="absolute left-0 top-50 w-60 h-50 bg-linear-to-t from-black/40 to-transparent"></div>

       <div v-if="canEdit && character.author.user_id === user.id" class="absolute right-0 top-50">
         <RouterLink @click.stop :to="{name:'update-character',params:{character_id:character.id}}" class="btn btn-circle btn-ghost bg-transparent">
           <UpdateIcon/>
         </RouterLink>
         <button @click.stop="handleRemoveCharacter" class="btn btn-circle btn-ghost bg-transparent">
           <RemoveIcon/>
         </button>
       </div>

       <div v-if="canRemoveFriend" class="absolute right-0 top-50">
         <button @click.stop="handleRemoveFriend" class="btn btn-circle btn-ghost bg-transparent">
           <RemoveIcon/>
         </button>
       </div>

       <div class="absolute left-4 top-54 avatar">
         <div class="w-16 rounded-full ring-3 ring-white">
           <img :src="character.photo" alt="">
         </div>
       </div>
       <div class="absolute left-24 right-4 top-58 text-white font-bold line-clamp-1 break-all">
         {{character.name}}
       </div>
       <div class="absolute left-4 right-4 top-72 text-white line-clamp-4 break-all">
         {{character.profile}}
       </div>
     </div>
   </div>
   <RouterLink :to="{name:'user-space-index',params:{user_id:character.author.user_id}}" class="flex items-center mt-4 gap-2 w-60">
     <div class="avatar">
       <div class="w-7 rounded-full">
         <img :src="character.author.photo" alt="">
       </div>
     </div>
     <div class="text-sm line-clamp-1 break-all">{{character.author.username}}</div>
   </RouterLink>
   <ChatField ref="chat-field-ref" :friend="friend"/>
 </div>
</template>

<style scoped>

</style>