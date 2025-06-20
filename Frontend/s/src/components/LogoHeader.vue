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
  background: linear-gradient(45deg, #409EFF, #3687de 33%, #61b0fe 100%);
  padding-left: 32px;
  font-size: 2rem;
  color: #fff;
  font-weight: bold;
  letter-spacing: 2px;
  user-select: none;
  box-shadow: 0 2px 8px rgba(64,158,255,0.5);
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
  -webkit-user-drag: none; /* Chrome, Safari */
  -moz-user-drag: none; /* Firefox */
  -ms-user-drag: none; /* Internet Explorer */
}
</style>
