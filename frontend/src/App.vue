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

  }finally {
    user.setHasPulledUserInfo(true)

    if(route.meta.needLogin && !user.isLogin()){
      await router.replace({
        name: 'user-account-login-index',
      })
    }
  }
})
</script>

<template>
  <div
    class="fixed inset-0 z-[-1] transition-all duration-500"
    :style="user.appBackground ? {
      backgroundImage: `url(${user.appBackground})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      /* 注意：这里移除了 backgroundAttachment: 'fixed'，因为外层使用了 fixed 定位，已经达到了固定视口的效果，且移动端兼容性更好 */
      backgroundColor: 'transparent'
    } : {
      backgroundColor: 'var(--fallback-b1,oklch(var(--b1)/1))'
    }"
  ></div>

  <div class="min-h-screen overflow-x-hidden">
    <NavBar>
      <RouterView />
    </NavBar>
  </div>
</template>

<style scoped>

</style>
