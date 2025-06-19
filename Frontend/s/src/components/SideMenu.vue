<template>
  <el-menu
    :default-active="activePath"
    class="side-menu"
    router
    background-color="#212121"
    text-color="#fff"
    active-text-color="#409EFF"
  >
    <el-menu-item index="/dashboard">
      <el-icon><HomeFilled /></el-icon>
      <span>可视化展示</span>
    </el-menu-item>
    <el-menu-item index="/analysis">
      <el-icon><DataAnalysis /></el-icon>
      <span>分析预测</span>
    </el-menu-item>
    <el-menu-item index="/settings">
      <el-icon><Setting /></el-icon>
      <span>模型训练</span>
    </el-menu-item>
  </el-menu>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import { HomeFilled, DataAnalysis, Setting } from '@element-plus/icons-vue'

const route = useRoute()
const activePath = computed(() => route.path)
</script>

<style scoped>
.side-menu {
  width: 210px;
  height: 100%;
  min-height: 0;
  border-right: 0;
  background: #212121;
  user-select: none;
  overflow: hidden; /* 侧栏不滚动！ */
  box-shadow: 4px 0px 10px 0 rgba(0, 0, 0, 0.6);;
}
</style>