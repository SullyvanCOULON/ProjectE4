<script setup lang="ts">
import DocsForm from './components/DocsForm.vue';

const props = defineProps<{
}>();
</script>
<template>
  <div class="admin-container d-flex flex-row justify-content-center align-items-center">
    <DocsForm/>
  </div>
</template>
<style scoped lang="scss">
  .admin-container {
    height: 100%;
  }
</style>
