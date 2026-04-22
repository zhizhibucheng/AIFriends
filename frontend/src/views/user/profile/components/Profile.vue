<script setup>
import {ref, watch} from "vue";

const props = defineProps(['profile'])
const myProfile = ref(props.profile)

watch(() => props.profile, newVal => {
  myProfile.value = newVal
})

defineExpose({
  myProfile,
})
</script>

<template>
 <fieldset class="fieldset w-full">
   <legend class="fieldset-legend text-base font-bold">简介</legend>
   <textarea v-model="myProfile" rows="6" class="textarea w-full bg-base-200/70"></textarea>
 </fieldset>
</template>

<style scoped>

</style>