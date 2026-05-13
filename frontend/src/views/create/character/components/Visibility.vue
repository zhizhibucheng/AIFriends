<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  isPublic: {
    type: Boolean,
    default: true
  }
});

const myIsPublic = ref(props.isPublic);

// 监听 props 变化（主要用于在更新角色时，后端数据返回后的响应式同步）
watch(() => props.isPublic, (newVal) => {
  myIsPublic.value = newVal;
});

// 将内部的值暴露给父组件调用
defineExpose({
  myIsPublic
});
</script>

<template>
  <fieldset class="fieldset mt-4 w-full">
    <legend class="fieldset-legend text-base font-bold">可见性状态</legend>
    <select v-model="myIsPublic" class="select select-bordered w-full bg-base-100/70">
      <option :value="true">公开</option>
      <option :value="false">私密</option>
    </select>
  </fieldset>
</template>