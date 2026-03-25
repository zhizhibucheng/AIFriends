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
    class="min-h-screen transition-all duration-500"
    :style="user.appBackground ? {
      backgroundImage: `url(${user.appBackground})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundAttachment: 'fixed',
      backgroundColor: 'transparent'
    } : {
      backgroundColor: 'var(--fallback-b1,oklch(var(--b1)/1))'
    }"
  >
    <NavBar >
      <RouterView />
    </NavBar>
  </div>

<!--  <NavBar >-->
<!--    <RouterView />-->
<!--  </NavBar>-->
</template>

<style scoped>

</style>
