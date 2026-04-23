import { createRouter, createWebHistory } from 'vue-router'
import HomepageIndex from "@/views/homepage/HomepageIndex.vue";
import FriendIndex from "@/views/friend/FriendIndex.vue";
import CreateIndex from "@/views/create/CreateIndex.vue";
import NotFoundIndex from "@/views/error/NotFoundIndex.vue";
import LoginIndex from "@/views/user/account/LoginIndex.vue";
import RegisterIndex from "@/views/user/account/RegisterIndex.vue";
import SpaceIndex from "@/views/user/space/SpaceIndex.vue";
import ProfileIndex from "@/views/user/profile/ProfileIndex.vue";
import {useUserStore} from "@/stores/user.js";
import UpdateCharacter from "@/views/create/character/UpdateCharacter.vue";
import VerifyIndex from "@/views/user/account/VerifyIndex.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/',
      component: HomepageIndex,
      name: 'homepage-index',
      meta:{
        needLogin:false,
      },
    },
    {
      path:'/friend/',
      component: FriendIndex,
      name: 'friend-index',
      meta:{
        needLogin:true,
        needVerified: true, // 新增：与角色互动必须实名
      },
    },
    {
      path:'/create/',
      component: CreateIndex,
      name: 'create-index',
      meta:{
        needLogin:true,
        needVerified: true, // 新增：创建角色必须实名
      },
    },
    {
      path:'/create/character/update/:character_id/',
      component: UpdateCharacter,
      name: 'update-character',
      meta:{
        needLogin:true,
        needVerified: true, // 新增：修改角色必须实名
      },
    },
    {
      path:'/user/verify/',
      component: VerifyIndex,
      name: 'user-verify-index',
      meta:{
        needLogin: true,
        needVerified: false, // 认证页面本身不需要再次认证
      },
    },
    {
      path:'/404/',
      component: NotFoundIndex,
      name: '404',
      meta:{
        needLogin:false,
      },
    },
    {
      path:'/user/account/login/',
      component: LoginIndex,
      name: 'user-account-login-index',
      meta:{
        needLogin:false,
      },
    },
    {
      path:'/user/account/register/',
      component: RegisterIndex,
      name: 'user-account-register-index',
      meta:{
        needLogin:false,
      },
    },
    {
      path:'/user/space/:user_id/',
      component: SpaceIndex,
      name: 'user-space-index',
      meta:{
        needLogin:false,
      },
    },
    {
      path:'/user/profile/',
      component: ProfileIndex,
      name: 'user-profile-index',
      meta:{
        needLogin:true,
      },
    },
    {
      path: '/:pathMatch(.*)*',
      component: NotFoundIndex,
      name: 'not-found',
      meta:{
        needLogin:false,
      },
    },
  ],
})

router.beforeEach((to, from) => {
  const user =useUserStore()
  if(to.meta.needLogin && user.hasPulledUserInfo &&!user.isLogin()){
    return{
      name:'user-account-login-index'
    }
  }
  // ==== 核心合规拦截区域 ====
  if(user.hasPulledUserInfo && user.isLogin()) {

    // 2. 实名认证拦截：如果目标页面需要实名，但用户未实名
    if (to.meta.needVerified && !user.isVerified) {
      // 强制重定向到实名认证页面
      return {
        name: 'user-verify-index'
      }
    }

    // 3. 新增：未成年人一刀切拦截
    // 如果用户是未成年人，且试图访问聊天相关页面（即 /friend/ 路由）
    if (user.isMinor && (to.name === 'friend-index' || to.path.startsWith('/friend'))) {
        // 弹出警告提示（你可以根据需要换成更优雅的组件如 ElMessage）
        alert('根据相关法规，未成年人无法使用本系统的AI互动聊天服务。')
        // 阻断跳转，停留在当前页（如果是直接输入网址，则退回首页）
        return from.name ? false : { name: 'homepage-index' }
    }
  }
  return true
})

export default router
