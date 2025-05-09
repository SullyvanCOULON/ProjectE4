<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import Chat from '@/features/user_chat/components/Chat/Chat.vue'

const messages = ref<{ from: 'user' | 'bot'; content: string }[]>([
  { from: 'bot', content: 'Bonjour' }
])

const messagesContainer = ref<HTMLDivElement | null>(null) // Référence pour cibler et gérer la zone de messages

function scrollToTop() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTo({ top: 0, behavior: 'smooth' }) // Remonte pour que les nouveaux messages soient visibles comme prévu avec column-reverse
    }
  })
}

async function handleSendMessage(content: string) {
  // Ajouter un message utilisateur
  messages.value.unshift({ from: 'user', content })

  try {
    const response = await fetch('http://localhost:5000/api/message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: content })
    })

    if (response.ok) {
      const data = await response.json()
      messages.value.unshift({ from: 'bot', content: data.response })
    } else {
      messages.value.unshift({ from: 'bot', content: 'Erreur de communication avec le serveur.' })
    }
  } catch (error) {
    console.error('Erreur réseau :', error)
    messages.value.unshift({ from: 'bot', content: 'Impossible de contacter le serveur.' })
  }

  scrollToTop()
}

// Scroller au bon endroit au montage pour assurer un bon affichage
onMounted(scrollToTop)
</script>

<template>
  <div class="user-chat" ref="messagesContainer">
    <Chat :messages="messages" @send-message="handleSendMessage" />
  </div>
</template>

<style scoped lang="scss">
@use '../../assets/scss/base.scss' as *;
@use '../../assets/scss/debug.scss' as *;

.user-chat {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.message {
  margin-bottom: 8px;
}

.message.user {
  text-align: right;
  color: #007bff;
}

.message.bot {
  text-align: left;
  color: #333;
}

.input-area {
  margin-bottom: 12px;
}
</style>