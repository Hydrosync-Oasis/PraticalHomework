<template>
  <Form :validation-schema="schema" :initial-values="initialValues" v-slot="{ handleSubmit }">
    <el-form class="form" @submit.prevent="handleSubmit(onSubmit)">
      
      <el-form-item label="怀孕次数" class="item">
        <Field name="pregnancies" v-slot="{ field }" as="div">
          <el-input-number v-bind="field" v-model="field.value" :min="0" :max="20" placeholder="请输入怀孕次数" />
        </Field>
        <div class="msg"><ErrorMessage name="pregnancies" /></div>
      </el-form-item>

      <el-form-item label="血糖浓度" class="item">
        <Field name="glucose" v-slot="{ field }" as="div">
          <el-input-number v-bind="field" v-model="field.value" :min="0" :max="300" placeholder="请输入血糖值" />
        </Field>
        <div class="msg"><ErrorMessage name="glucose" /></div>
      </el-form-item>

      <el-form-item label="血压" class="item">
        <Field name="blood_pressure" v-slot="{ field }" as="div">
          <el-input-number v-bind="field" v-model="field.value" :min="0" :max="200" placeholder="请输入舒张压" />
        </Field>
        <div class="msg"><ErrorMessage name="blood_pressure" /></div>
      </el-form-item>

      <el-form-item label="皮褶厚度" class="item">
        <Field name="skin_thickness" v-slot="{ field }" as="div">
          <el-input-number v-bind="field" v-model="field.value" :min="0" :max="100" placeholder="请输入皮褶厚度" />
        </Field>
        <div class="msg"><ErrorMessage name="skin_thickness" /></div>
      </el-form-item>

      <el-form-item label="胰岛素" class="item">
        <Field name="insulin" v-slot="{ field }" as="div">
          <el-input-number v-bind="field" v-model="field.value" :min="0" :max="900" placeholder="请输入胰岛素数值" />
        </Field>
        <div class="msg"><ErrorMessage name="insulin" /></div>
      </el-form-item>

      <el-form-item label="BMI" class="item">
        <Field name="bmi" v-slot="{ field }" as="div">
          <el-input-number v-bind="field" v-model="field.value" :step="0.1" :min="0" :max="70" placeholder="请输入BMI" />
        </Field>
        <div class="msg"><ErrorMessage name="bmi" /></div>
      </el-form-item>

      <el-form-item label="糖尿病家族指数" class="item">
        <Field name="diabetes_pedigree_function" v-slot="{ field }" as="div">
          <el-input-number v-bind="field" v-model="field.value" :step="0.001" :min="0" :max="3" placeholder="请输入遗传指数" />
        </Field>
        <div class="msg"><ErrorMessage name="diabetes_pedigree_function" /></div>
      </el-form-item>

      <el-form-item label="年龄" class="item">
        <Field name="age" v-slot="{ field }" as="div">
          <el-input-number v-bind="field" v-model="field.value" :min="0" :max="150" placeholder="请输入年龄" />
        </Field>
        <div class="msg"><ErrorMessage name="age" /></div>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" native-type="submit">提交</el-button>
      </el-form-item>
    </el-form>
  </Form>
</template>

<script setup>
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import { readonly } from 'vue'

const emit = defineEmits(['submit'])

const initialValues = {
  pregnancies: 0,
  glucose: 80,
  blood_pressure: 70,
  skin_thickness: 20,
  insulin: 0,
  bmi: 20.0,
  diabetes_pedigree_function: 0.0,
  age: 30
}

const schema = readonly(
  yup.object({
    pregnancies: yup.number().required().min(0).max(20),
    glucose: yup.number().required().min(0).max(300),
    blood_pressure: yup.number().required().min(0).max(200),
    skin_thickness: yup.number().required().min(0).max(100),
    insulin: yup.number().required().min(0).max(900),
    bmi: yup.number().required().min(0).max(70),
    diabetes_pedigree_function: yup.number().required().min(0).max(3),
    age: yup.number().required().min(0).max(150)
  })
)

function onSubmit(values) {
  console.log('预测输入数据:', values)
  emit('submit', values)
}
</script>

<style scoped>
.form {
  max-width: 500px;
  margin: auto;
}
.item {
  margin-bottom: 30px;
}
.msg {
  color: red;
  font-size: 12px;
}
</style>
