<script setup>
import MenuIcon from "@/components/navbar/icons/MenuIcon.vue";
import HomePageIcon from "@/components/navbar/icons/HomePageIcon.vue";
import FriendIcon from "@/components/navbar/icons/FriendIcon.vue";
import CreateIcon from "@/components/navbar/icons/CreateIcon.vue";
import SearchIcon from "@/components/navbar/icons/SearchIcon.vue";
import {useUserStore} from "@/stores/user.js";
import UserMenu from "@/components/navbar/UserMenu.vue";
import {ref, watch} from "vue";
import {useRoute, useRouter} from "vue-router";

const user = useUserStore()
const searchQuery = ref('')
const router = useRouter()
const route = useRoute()

watch(()=> route.query.q,newQ => {
  searchQuery.value = newQ || ''
})
function handleSearch(){
  router.push({
    name: 'homepage-index',
    query: {
      q: searchQuery.value.trim(),
    }
  })
}
</script>

<template>
  <div class="drawer lg:drawer-open bg-transparent h-full">
    <input id="my-drawer-4" type="checkbox" class="drawer-toggle" />

    <div class="drawer-content bg-transparent flex flex-col h-full overflow-hidden relative">

      <nav class="navbar w-full bg-base-100/10 backdrop-blur-xl shadow-sm z-50 flex-none">

        <div class="navbar-start w-auto flex items-center">
          <label for="my-drawer-4" aria-label="open sidebar" class="btn btn-square btn-ghost">
            <MenuIcon />
          </label>
          <div class="px-2 font-bold text-xl flex items-center gap-2">
            <img src="/favicon.ico" alt="Logo" class="w-8 h-8" />
            <span class="hidden sm:block">AIFriends</span>
          </div>
        </div>

        <div class="navbar-center flex-1 flex justify-center px-2">
          <form @submit.prevent="handleSearch" class="join w-full max-w-xl flex justify-center">
            <input v-model="searchQuery" class="input join-item rounded-l-full w-full bg-base-200/40 min-w-0 px-3 text-sm sm:text-base" placeholder="搜索内容" />
            <button class="btn join-item rounded-r-full gap-1 bg-base-200/20 border-none hover:bg-base-300 px-3 sm:px-4">
              <SearchIcon />
              <span class="hidden sm:inline">搜索</span>
            </button>
          </form>
        </div>

        <div class="navbar-end w-auto">
          <RouterLink v-if="user.isLogin()" :to="{name:'create-index'}" active-class="btn-active" class="btn btn-ghost text-base sm:mr-6 px-2 sm:px-4">
            <CreateIcon />
            <span class="hidden sm:inline">创作</span>
          </RouterLink>
          <RouterLink v-if="user.hasPulledUserInfo && !user.isLogin()" :to="{name:'user-account-login-index'}" active-class="btn-active" class="btn btn-ghost text-base sm:text-lg px-3 sm:px-4">
            登录
          </RouterLink>
          <UserMenu v-else-if="user.isLogin()" />
        </div>

      </nav>

      <div class="flex-1 overflow-y-auto flex flex-col">

        <div class="flex-grow">
          <slot></slot>
        </div>

        <footer class="footer footer-center p-4 py-6 bg-transparent mt-auto">
          <div class="flex flex-col sm:flex-row gap-2 sm:gap-6 items-center justify-center w-full">

            <p class="flex items-center gap-1">
              <img :src="'/static/frontend/images/foot-icp.png'" class="w-4 h-4" alt="ICP备案">
              <a href="https://beian.miit.gov.cn/" target="_blank"
                 class="text-slate-100 hover:text-primary transition-all font-semibold drop-shadow-md text-xs sm:text-sm">
                晋ICP备2026003601号-1
              </a>
            </p>

            <p class="flex items-center gap-1">
              <img :src="'/static/frontend/images/foot-ga.png'" class="w-4 h-4" alt="公安备案">
              <a href="https://beian.mps.gov.cn/#/query/webSearch?code=14010902001851" target="_blank"
                 class="text-slate-100 hover:text-primary transition-all font-semibold drop-shadow-md text-xs sm:text-sm">
                晋公网安备14010902001851号
              </a>
            </p>

          </div>
        </footer>

      </div>
      </div>

    <div class="drawer-side is-drawer-close:overflow-visible z-[60] h-full">
      <label for="my-drawer-4" aria-label="close sidebar" class="drawer-overlay"></label>

      <div class="flex h-full flex-col items-start bg-base-200/40 backdrop-blur-xl is-drawer-close:w-16 is-drawer-open:w-54 border-r border-base-content/5">
        <ul class="menu w-full grow">
          <li>
            <RouterLink :to="{name:'homepage-index'}" active-class="menu-focus" class="is-drawer-close:tooltip-right py-3" data-tip="首页">
              <HomePageIcon />
              <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">首页</span>
            </RouterLink>
          </li>
          <li>
            <RouterLink :to="{name:'friend-index'}" active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="好友">
              <FriendIcon />
              <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">好友</span>
            </RouterLink>
          </li>
          <li>
            <RouterLink :to="{name:'create-index'}" active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="创作">
              <CreateIcon />
              <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">创作</span>
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>