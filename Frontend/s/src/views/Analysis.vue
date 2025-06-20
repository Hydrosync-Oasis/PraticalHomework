<template>
    <el-container>
        <el-header>
            <h1>
                填写题目，获取你的肺癌患病率：
            </h1>
        </el-header>
        <el-main>
            <el-steps :active="1">
                <el-step title="基本信息" description="年龄与性别"></el-step>
                <el-step title="疾病史" description=""></el-step>
                <el-step title="症状" description="劳累、气喘、焦虑"></el-step>
            </el-steps>

            <div class="form">
                <BasicForm @submit="F"></BasicForm>
            </div>
        </el-main>
    </el-container>
</template>

<script setup>
import BasicForm from './Forms/BasicInfo.vue'

function F() {
    console.log('接收到了事件')
}
</script>

<style scoped>
.form {
    width: 30%;
    min-width: 580px;
    margin-left: auto;
    margin-right: auto;
    border: 2px gray;
}
</style>