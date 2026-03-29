<script setup>

import {ref, watch} from "vue";

const props = defineProps(['name'])
const myName = ref(props.name)

watch(() => props.name, newVal => {
  myName.value = newVal
})

defineExpose({
  myName,
})
</script>

<template>
 <fieldset class="fieldset w-full">
   <label class="label text-base">名字</label>
   <input v-model="myName" type="text" class="input w-full bg-base-100/70">
 </fieldset>
</template>

<style scoped>

</style>