<script setup>
defineProps(['userProfile'])
</script>

<template>
 <div v-if="userProfile" class="flex flex-col sm:flex-row items-center mt-6 sm:mt-12 gap-4 sm:gap-8 w-11/12 sm:w-auto max-w-full">

   <div class="avatar">
     <div class="w-28 sm:w-44 rounded-full shadow-md">
       <img :src="userProfile.photo" alt="用户头像" />
     </div>
   </div>

   <div class="flex flex-col justify-center items-center sm:items-start w-full sm:w-64">
     <div class="text-xl sm:text-2xl font-bold line-clamp-1 break-all text-center sm:text-left">
       {{userProfile.username}}
     </div>
     <div class="text-xs sm:text-sm text-gray-500 mt-1 sm:mt-2">
       AIFriends号:{{userProfile.user_id}}
     </div>
     <div class="text-sm h-auto sm:h-20 mt-3 sm:mt-4 line-clamp-4 break-all text-center sm:text-left px-4 sm:px-0 text-base-content/80">
       {{userProfile.profile}}
     </div>
   </div>

 </div>
</template>

<style scoped>

</style>