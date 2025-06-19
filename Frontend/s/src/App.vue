<template>
  <div class="app-container">
    <LogoHeader />
    <div class="main-wrapper">
      <SideMenu />
      <main class="content-area">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import LogoHeader from './components/LogoHeader.vue'
import SideMenu from './components/SideMenu.vue'


</script>

<style>
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden; /* 页面整体无滚动条 */
}
.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
.main-wrapper {
  flex: 1;
  display: flex;
  min-height: 0; /* 防止内容撑出溢出 */
  height: 0;
  background: #eef5fd;
}
/* 侧栏不滚动，高度自动填满 */
</style>
