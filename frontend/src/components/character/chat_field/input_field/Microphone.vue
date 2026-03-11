<script setup>
import KeyboardIcon from "@/components/character/icons/KeyboardIcon.vue";

const emit = defineEmits(['close'])
</script>

<template>
 <div class="absolute bottom-4 left-2 h-12 w-86 flex items-center bg-black/30 backdrop-blur-sm rounded-2xl">
   <div class="text-white/50 text-base w-full text-center">
     语音输入
   </div>
   <div @click="emit('close')" class="absolute right-2 w-8 h-8 flex justify-center items-center cursor-pointer">
     <KeyboardIcon/>
   </div>
 </div>
</template>

<style scoped>

</style>