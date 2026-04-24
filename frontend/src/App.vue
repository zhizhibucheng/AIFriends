<script setup>

import NavBar from "@/components/navbar/NavBar.vue";
import {onMounted} from "vue";
import {useUserStore} from "@/stores/user.js";
import api from "@/js/http/api.js";
import {useRoute, useRouter} from "vue-router";

const user = useUserStore()
const route =useRoute()
const router = useRouter()

onMounted(async ()=>{
  try{
    const res=await api.get('/api/user/account/get_user_info/')
    const data = res.data
    if(data.result === 'success'){
      user.setUserInfo(data)
    }
  }catch(error){

  }

  user.setHasPulledUserInfo(true)

  if(route.meta.needLogin && !user.isLogin()){
    await router.replace({
      name: 'user-account-login-index',
    })
    return
  }
    // 2. 实名认证检查：已登录但访问需要认证的页面，且用户未认证
  if (user.isLogin() && route.meta.needVerified && !user.isVerified) {
    await router.replace({ name: 'user-verify-index' })
    return
  }

    // 3. 未成年人一刀切拦截
  if (user.isLogin() && user.isMinor && (route.name === 'friend-index' || route.path.startsWith('/friend'))) {
    alert('根据相关法规，未成年人无法使用本系统的AI互动聊天服务。')
    await router.replace({ name: 'homepage-index' })
  }

})
</script>

<template>
  <div
    class="fixed inset-0 z-[-1] transition-all duration-500"
    :style="{
      /* 始终保留底色，防止图片加载瞬间变白 */
      backgroundColor: 'var(--fallback-b1,oklch(var(--b1)/1))',
      /* 只有当图片存在时才叠加背景图 */
      ...(user.appBackground ? {
        backgroundImage: `url(${user.appBackground})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      } : {})
    }"
  ></div>

  <div class="h-screen overflow-hidden">
    <NavBar>
      <RouterView />
    </NavBar>
  </div>
</template>

<style scoped>

</style>
