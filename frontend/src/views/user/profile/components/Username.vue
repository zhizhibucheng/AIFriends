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
    <label class="label text-base">用户名</label>
    <input v-model="myUsername" type="text" class="input w-full bg-base-200/70">
  </fieldset>
</template>

<style scoped>

</style>