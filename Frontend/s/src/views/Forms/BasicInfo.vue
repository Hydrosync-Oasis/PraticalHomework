<template>
  <Form :validation-schema="schema" v-slot="{ handleSubmit }">
    <el-form class="form" @submit.prevent="handleSubmit(onSubmit)">
      <el-form-item label="性别" class="item">
        <Field name="gender" v-slot="{ field }">
          <el-select v-bind="field" v-model="field.value" placeholder="请选择性别">
            <el-option label="男" value="M" />
            <el-option label="女" value="F" />
          </el-select>
        </Field>
        <div class="msg"><ErrorMessage name="gender" /></div>
      </el-form-item>

      <el-form-item label="年龄" class="item">
        <Field name="age" v-slot="{ field }">
          <el-input v-bind="field" v-model.number="field.value" placeholder="请输入年龄" />
        </Field>
        <div class="msg"><ErrorMessage name="age" /></div>
      </el-form-item>

      <el-form-item label="是否吸烟" class="item">
        <Field name="smoking" v-slot="{ field }">
          <el-switch v-bind="field" v-model="field.value" />
        </Field>
        <div class="msg"><ErrorMessage name="smoking" /></div>
      </el-form-item>

      <el-form-item label="是否饮酒" class="item">
        <Field name="alcohol" v-slot="{ field }">
          <el-switch v-bind="field" v-model="field.value" />
        </Field>
        <div class="msg"><ErrorMessage name="alcohol" /></div>
      </el-form-item>

      <el-form-item label="同伴压力" class="item">
        <Field name="peerPressure" v-slot="{ field }">
          <el-switch v-bind="field" v-model="field.value" />
        </Field>
        <div class="msg"><ErrorMessage name="peerPressure" /></div>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" native-type="submit">提交</el-button>
      </el-form-item>
    </el-form>
  </Form>
</template>

<script setup>
import { Form, Field, ErrorMessage } from 'vee-validate';
import { readonly } from 'vue';
import * as yup from 'yup';

const emit = defineEmits(['submit'])

const schema = readonly(yup.object({
  gender: yup.string().required('请选择性别'),
  age: yup.number().typeError('请输入数字').required('请输入年龄').min(0).max(150),
  smoking: yup.boolean().required().default(false),
  alcohol: yup.boolean().required().default(false),
  peerPressure: yup.boolean().required().default(false)
}))

function onSubmit(values) {
  console.log('提交数据', values);
  emit('submit', values);
}
</script>

<style scoped>
.msg {
  color: red;
  font-size: 12px;
}
.item {
  margin-bottom: 40px;
}
</style>
