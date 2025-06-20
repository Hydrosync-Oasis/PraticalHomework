<template>
    <el-container>
        <el-header>
            <h1>
                填写题目，获取你的肺癌患病率：
            </h1>
        </el-header>
        <el-main>
            <el-steps :active="index">
                <el-step title="基本信息" description="年龄与性别"></el-step>
                <el-step title="疾病史" description=""></el-step>
                <el-step title="症状" description="劳累、气喘、焦虑"></el-step>
            </el-steps>

            <div class="form">
                <component :is="components[index]" @submit="F">
                </component>
            </div>
        </el-main>
    </el-container>
</template>

<script setup>
import BasicForm from './Forms/BasicInfo.vue'
import DiseaseForm from './Forms/Disease.vue'
import SymptomForm from './Forms/Symptom.vue'
import { ref } from 'vue'

const components = [BasicForm, DiseaseForm, SymptomForm];
const formsData = [];
const index = ref(0);   

function F(values) {
    console.log(index.value)
    if (index.value == components.length - 1) {
        return;
    }
    formsData[index.value] = values;
    index.value++;
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