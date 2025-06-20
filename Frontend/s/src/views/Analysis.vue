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
            
        </el-main>
    </el-container>
</template>

<script setup>
import { Form, Field, ErrorMessage } from 'vee-validate';
import { readonly } from 'vue';
import * as yup from 'yup';

const schema = readonly(yup.object(
    {
        gender: yup.string().required('请选择性别'),
        age: yup.number()
            .typeError('请输入数字')
            .required('请输入年龄')
            .min(0, '年龄不能为负数')
            .max(150, '年龄过大'),
    }
))

function onSubmit(values) {
  // 校验通过后，数据在这里
  console.log('提交数据', values)
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