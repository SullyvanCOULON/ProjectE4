<script setup lang="ts">
import "@/assets/scss/base.scss"
import TheHeader from './components/Header.vue';
import TheFooter from './components/Footer.vue';
import { reactive, type Component as C } from 'vue';
import type { Page } from './interfaces'
import UserChat from '@/features/user_chat/UserChat.vue'
import Admin from '@/features/admin/Admin.vue'
const state = reactive<{
  page: Page
}>({
  page: 'UserChat'
})
const pages: { [s: string]: C } = {
  UserChat,
  Admin
}
function navigate(page: Page): void {
  state.page = page;
}

console.log(state.page);  // Pour vérifier la page au démarrage
</script>

<template>
  <div class="app-container">
    <TheHeader class="header" :page="state.page" @navigate="navigate"/>
    <div class="app-content">
      <Component :is="pages[state.page]"/>
    </div>
    <TheFooter class="footer" />
  </div>
</template>

<style lang="scss">
.app-container {
  min-height: 100vh;
  display: grid;
  grid-template-areas: 'header' 'app-content' 'footer';
  grid-template-rows: 48px auto 48px;
}
.header { grid-area: header;}
.app-content {
  grid-area: app-content;
  height: 100%;
  overflow: hidden;
}
.footer { grid-area: footer;}
</style>
