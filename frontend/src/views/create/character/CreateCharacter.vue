<script setup>

import Photo from "@/views/create/character/components/Photo.vue";
import Name from "@/views/create/character/components/Name.vue";
import Profile from "@/views/create/character/components/Profile.vue";
import BackgroundImage from "@/views/create/character/components/BackgroundImage.vue";
import {useTemplateRef} from "vue";

const photoRef = useTemplateRef('photo-ref')
const nameRef = useTemplateRef('name-ref')
const profileRef = useTemplateRef('profile-ref')
const backgroundImageRef = useTemplateRef('background-image-ref')
</script>

<template>
 <div class="flex justify-center">
   <div class="card w-120 bg-base-200 shadow-sm mt-16">
     <div class="card-body">
       <h3 class="text-lg font-bold my-4">创建角色</h3>
       <Photo ref="photo-ref"/>
       <Name ref="name-ref"/>
       <Profile ref="profile-ref"/>
       <BackgroundImage ref="background-image-ref"/>
       <div class="flex justify-center">
         <button class="btn btn-neutral w-60 mt-2">创建</button>
       </div>
     </div>
   </div>
 </div>
</template>

<style scoped>

</style>