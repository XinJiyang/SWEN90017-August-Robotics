<template>
  <div class="app">
    <component :is="currentLayout"></component>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import LoginLayout from './layouts/login-layout.vue';
import MainLayout from './layouts/main-layout.vue';


const currentLayout = computed(() => {
  return (useRoute().path === '/login' || useRoute().path === '/register') ? LoginLayout : MainLayout;
});
</script>

<style lang="less" scoped>
.app {
  width: 100vw;
  height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
</style>
