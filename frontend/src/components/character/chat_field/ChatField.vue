<script setup>
import {computed, nextTick, ref, useTemplateRef} from "vue";
import InputField from "@/components/character/chat_field/input_field/InputField.vue";
import CharacterPhotoField from "@/components/character/chat_field/character_photo_field/CharacterPhotoField.vue";
import ChatHistory from "@/components/character/chat_field/chat_history/ChatHistory.vue";
import AvatarCompanion from "@/components/character/AvatarCompanion.vue";

const props = defineProps(['friend'])
const modalRef = useTemplateRef('modal-ref')
const inputRef = useTemplateRef('input-ref')
const chatHistoryRef = useTemplateRef('chat-history-ref')
const history = ref([])

// 新增：精确控制聊天框是打开还是关闭状态
const isOpen = ref(false)

async function showModal() {
  isOpen.value = true // 打开时设为 true
  modalRef.value.showModal()

  await nextTick()
  inputRef.value.focus()
}

const modalStyle = computed(() => {
  if (props.friend) {
    return {
      backgroundImage: `url(${props.friend.character.background_image})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
    }
  } else {
    return {}
  }
})

function handlePushBackMessage(msg) {
  history.value.push(msg)
  chatHistoryRef.value.scrollToBottom()
}

function handleAddToLastMessage(delta) {
  history.value.at(-1).content += delta
  chatHistoryRef.value.scrollToBottom()
}

function handlePushFrontMessage(msg) {
  history.value.unshift(msg)
}

function handleClose() {
  isOpen.value = false // 关闭时设为 false，彻底销毁 3D 模型
  inputRef.value.close()
}

function handleKeyboardPop() {
  const delays = [100, 300, 500];
  delays.forEach(delay => {
    setTimeout(() => {
      if (chatHistoryRef.value) {
        chatHistoryRef.value.scrollToBottom()
      }
    }, delay)
  })
}

defineExpose({
  showModal,
})
</script>

<template>
  <dialog ref="modal-ref" class="modal" @close="handleClose">
    <div class="relative flex items-center justify-center w-full h-full pointer-events-none">

      <div class="modal-box relative w-90 h-[85vh] max-h-[600px] pointer-events-auto" :style="modalStyle">
        <button @click="modalRef.close()"
                class="btn btn-sm btn-circle btn-ghost bg-transparent absolute right-1 top-1 z-50">✕
        </button>
        <ChatHistory
            ref="chat-history-ref"
            v-if="friend"
            :history="history"
            :friendId="friend.id"
            :character="friend.character"
            @pushFrontMessage="handlePushFrontMessage"
        />
        <InputField
            v-if="friend"
            ref="input-ref"
            :friendId="friend.id"
            @pushBackMessage="handlePushBackMessage"
            @addToLastMessage="handleAddToLastMessage"
            @focus="handleKeyboardPop"
        />
        <CharacterPhotoField v-if="friend" :character="friend.character"/>
      </div>

      <AvatarCompanion
          v-if="isOpen && friend && friend.character"
          :avatarType="friend.character.avatar_type"
      />

    </div>
  </dialog>
</template>

<style scoped>
</style>