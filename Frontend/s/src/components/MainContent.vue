<!-- components/MainContent.vue -->
<template>
  <section class="main-content">
    <div class="content-title">欢迎来到大屏展示区</div>
    <!-- 示例：可插入echarts、表格、卡片等 -->
    <el-card class="dashboard-card">
      <div style="font-size:22px;text-align:center;line-height:2;">
        这里是可视化大屏内容区域<br>
        <span style="font-size:14px;color:#999;">（可根据左侧菜单切换不同内容）</span>
      </div>
    </el-card>
  </section>
</template>

<style scoped>
.main-content {
  flex: 1;
  background: linear-gradient(135deg, #f4faff 60%, #f0f5ff 100%);
  padding: 32px;
  min-height: 100vh;
}
.content-title {
  font-size: 24px;
  color: #409EFF;
  margin-bottom: 24px;
  font-weight: bold;
  letter-spacing: 1.5px;
}
.dashboard-card {
  border-radius: 18px;
  box-shadow: 0 2px 24px rgba(64,158,255,0.13);
  background: #fff;
  margin-bottom: 28px;
  padding: 48px 0;
}
/* App.vue 里补充 */
.content-area {
  flex: 1;
  min-width: 0;
  min-height: 0;
  height: 100%;
  overflow-y: auto; /* 只有内容区有滚动条 */
  background: linear-gradient(135deg, #f4faff 60%, #f0f5ff 100%);
  padding: 32px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

</style>
