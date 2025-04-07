<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue'

const props = defineProps<{
  messages: { from: 'user' | 'bot'; content: string }[]
}>()

const emit = defineEmits<{
  (e: 'sendMessage', content: string): void;
}>()

const inputText = ref('')
const messagesContainer = ref<HTMLElement | null>(null)

function send() {
  if (inputText.value.trim()) {
    emit('sendMessage', inputText.value.trim())
    inputText.value = ''
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

onMounted(scrollToBottom)
watch(() => props.messages.length, scrollToBottom)
</script>

<template>
  <div class="chat-wrapper">
    <div class="messages" ref="messagesContainer">
      <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message', msg.from]"
      >
        {{ msg.content }}
      </div>
    </div>

    <div class="input-area">
      <textarea
          v-model="inputText"
          class="chat-input"
          placeholder="Écrivez un message..."
          @keydown.enter.prevent.exact="send"
          rows="1"
      />
      <button class="send-btn" @click="send">Envoyer</button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.chat-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.messages {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column-reverse; // Pour que les messages commencent en bas
  padding: 12px 8px;
}

.message {
  max-width: 70%;
  padding: 8px 12px;
  border-radius: 16px;
  line-height: 1.4;
  word-wrap: break-word;

  &.bot {
    background-color: #f0f0f0;
    align-self: flex-start;
  }

  &.user {
    background-color: #cce5ff;
    align-self: flex-end;
  }
}

.input-area {
  display: flex;
  gap: 8px;
  align-items: flex-end;
  border-top: 1px solid #ddd;
  padding-top: 8px;
  padding-bottom: env(safe-area-inset-bottom); /* pour iOS */
  background-color: white;
  margin-bottom: 12px;
  margin-left: 5px;
}

.chat-input {
  flex: 1;
  resize: none;
  max-height: 150px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  overflow-y: auto;
}

.send-btn {
  background-color: #41b883;
  border: none;
  color: white;
  font-weight: bold;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  height: 100%; /* S'assure que le bouton a la même hauteur que l'input */
  display: flex;
  align-items: center; /* Centrer le texte à l'intérieur du bouton */
  justify-content: center; /* Centrer le texte à l'intérieur du bouton */
  margin-right: 5px;

  &:hover {
    background-color: #368f6e;
  }
}
</style>