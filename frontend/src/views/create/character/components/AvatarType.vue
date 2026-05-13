<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
    avatarType: {
        type: String,
        default: 'none'
    },
    // 新增：是否禁用下拉框
    disabled: {
        type: Boolean,
        default: false
    }
});

const myAvatarType = ref('none');

onMounted(() => {
    if (props.avatarType) {
        myAvatarType.value = props.avatarType;
    }
});

// 监听异步数据：由于更新页面的数据是接口请求回来的，需要监听变化才能正确回显
watch(() => props.avatarType, (newVal) => {
    if (newVal) {
        myAvatarType.value = newVal;
    }
});

// 暴露给父组件，以便提交表单时获取选中的值
defineExpose({
    myAvatarType
});
</script>

<template>
  <fieldset class="fieldset mt-4 w-full">
    <legend class="fieldset-legend text-base font-bold">3D 实体形态 (伴随模型)</legend>
    <select
      v-model="myAvatarType"
      :disabled="props.disabled"
      class="select select-bordered w-full bg-base-100/70 disabled:bg-base-200 disabled:text-gray-400 disabled:cursor-not-allowed"
    >
      <option value="none">无</option>
      <option value="male">男性</option>
      <option value="female">女性</option>
      <option value="dog">小狗 (暂无，敬请期待)</option>
      <option value="cat">小猫 (暂无，敬请期待)</option>
    </select>
  </fieldset>
</template>