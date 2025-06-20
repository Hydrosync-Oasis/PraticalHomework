<template>
  <el-menu
    :default-active="activePath"
    class="side-menu"
    router
    background-color="#212121"
    text-color="#fff"
    active-text-color="#409EFF"
    :unique-opened="true"
  >
    <el-sub-menu index="/dashboard">
      <template #title>
        <el-icon><HomeFilled /></el-icon>
        <span>可视化展示</span>
      </template>
      <el-menu-item index="/dashboard/age">
        <el-icon><Calendar /></el-icon>
        <span>年龄分析</span>
      </el-menu-item>
      <el-menu-item index="/dashboard/gender">
        <el-icon><User /></el-icon>
        <span>性别分析</span>
      </el-menu-item>
      <el-menu-item index="/dashboard/correlation">
        <el-icon><Connection /></el-icon>
        <span>相关性分析</span>
      </el-menu-item>
      <el-menu-item index="/dashboard/smoking">
        <el-icon><Smoking /></el-icon>
        <span>吸烟分析</span>
      </el-menu-item>
    </el-sub-menu>
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
import { HomeFilled, DataAnalysis, Setting, Calendar, User, Connection, Smoking } from '@element-plus/icons-vue'

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
  box-shadow: 4px 0px 10px 0 rgba(0, 0, 0, 0.6);
}

:deep(.el-sub-menu__title) {
  padding-left: 20px !important;
}

:deep(.el-menu-item) {
  padding-left: 40px !important;
}

:deep(.el-sub-menu .el-menu-item) {
  background-color: #1a1a1a;
}

:deep(.el-sub-menu .el-menu-item.is-active) {
  background-color: #0c2135;
}
</style>