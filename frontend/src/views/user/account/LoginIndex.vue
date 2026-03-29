<script setup>
import {ref} from "vue";
import {useUserStore} from "@/stores/user.js";
import {useRouter} from "vue-router";
import api from "@/js/http/api.js";

const username =ref('')
const password =ref('')
const errorMessage = ref('')

const user = useUserStore()
const router = useRouter()

async function handleLogin() {
  errorMessage.value=''
  if(!username.value.trim()){
    errorMessage.value='用户名不能为空'
  }else if(!password.value.trim()){
    errorMessage.value='密码不能为空'
  }else{
    try{
      const res =await api.post('/api/user/account/login/',{
        username:username.value,
        password:password.value,
      })
      const data= res.data
      if(data.result === 'success'){
        user.setAccessToken(data.access)
        user.setUserInfo(data)
        await router.push({
          name: 'homepage-index'
        })
      }else{
        errorMessage.value = data.result
      }
    }catch(err){

    }
  }
}
</script>

<template>
  <div class="flex justify-center mt-30">
    <form @submit.prevent="handleLogin" class="fieldset bg-base-200/20 border-base-300 rounded-box w-xs border p-4">
      <label class="label">
        <span class="label-text text-base text-gray-700 font-bold">用户名</span>
      </label>
       <input
          v-model="username"
          type="text"
          class="input input-bordered bg-base-100/70 text-base-content placeholder-gray-400"
          placeholder="用户名"
       />

     <label class="label">
       <span class="label-text text-base text-gray-700 font-bold">密码</span>
     </label>
      <input
        v-model="password"
        type="password"
        class="input input-bordered bg-base-100/70 text-base-content placeholder-gray-400"
        placeholder="密码"
      />

     <p v-if="errorMessage" class="text-sm text-red-500 mt-1">{{errorMessage}}</p>

     <button class="btn btn-neutral mt-4">登录</button>
     <div class="flex justify-end">
       <RouterLink :to="{name:'user-account-register-index'}" class="btn btn-md btn-ghost text-gray-500">
         注册
       </RouterLink>
     </div>
    </form>

  </div>
</template>

<style scoped>

</style>