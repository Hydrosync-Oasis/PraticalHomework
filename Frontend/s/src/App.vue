<template>
  <div class="app-container">
    <LogoHeader />
    <div class="main-wrapper">
      <div class="sidebar-container" v-show="!sidebarCollapsed">
        <SideMenu />
      </div>
      <main class="content-area" :class="{'full-width': sidebarCollapsed}">
        <router-view v-slot="{ Component }">
          <keep-alive exclude="Analysis,Diabetes">
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import LogoHeader from './components/LogoHeader.vue'
import SideMenu from './components/SideMenu.vue'

// 侧边栏折叠状态
const sidebarCollapsed = ref(false)

// 监听自定义事件
function handleToggleSidebar(event) {
  sidebarCollapsed.value = event.detail.collapsed
}

onMounted(() => {
  window.addEventListener('toggle-sidebar', handleToggleSidebar)
})

onUnmounted(() => {
  window.removeEventListener('toggle-sidebar', handleToggleSidebar)
})
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
  background: #eef5fd;
  position: relative;
}
.sidebar-container {
  width: 210px;
  min-width: 210px;
  height: 100%;
  z-index: 10;
  overflow: hidden;
  position: relative;
  transition: all 0.3s ease;
}
.content-area {
  flex: 1;
  height: 100%;
  overflow-y: auto;
  padding: 0;
  box-sizing: border-box;
  position: relative;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}
.full-width {
  width: 100%;
}
</style>
