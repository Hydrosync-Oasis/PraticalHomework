<template>
  <header class="logo-header">
    <div class="logo">
      <div>
        Lung Cancer预测系统
      </div>

      <span>
        <img src="../assets/logo.png" alt="肺癌预测">
      </span>
    </div>
  </header>
</template>

<style scoped>
.logo-header {
  height: 100px;
  background: linear-gradient(90deg, #409EFF, #66b1ff 80%);
  padding-left: 32px;
  font-size: 2rem;
  color: #fff;
  font-weight: bold;
  letter-spacing: 2px;
  user-select: none;
  box-shadow: 0 2px 8px rgba(64,158,255,.09);
}

.logo {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.logo > div  {
  line-height: 100px;
}

img {
  width: 100px;
}
</style>
