<script setup>
import {ref, watch} from "vue";

const props = defineProps(['username'])
const myUsername = ref(props.username)

watch(() => props.username, newVal => {
  myUsername.value = newVal
})

defineExpose({
  myUsername,
})
</script>

<template>
  <fieldset class="fieldset w-full">
    <legend class="fieldset-legend text-base font-bold">用户名</legend>
    <input v-model="myUsername" type="text" class="input w-full bg-base-200/70">
  </fieldset>
</template>

<style scoped>

</style>