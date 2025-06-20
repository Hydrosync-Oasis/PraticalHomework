<template>
  <Form :validation-schema="schemaDisease" v-slot="{ handleSubmit }">
    <el-form class="form" @submit.prevent="handleSubmit(onSubmitDisease)">
      <el-form-item label="慢性疾病" class="item">
        <Field name="chronic" v-slot="{ field }">
          <el-switch v-bind="field" v-model="field.value" />
        </Field>
        <div class="msg"><ErrorMessage name="chronic" /></div>
      </el-form-item>

      <el-form-item label="过敏反应" class="item">
        <Field name="allergy" v-slot="{ field }">
          <el-switch v-bind="field" v-model="field.value" />
        </Field>
        <div class="msg"><ErrorMessage name="allergy" /></div>
      </el-form-item>

      <el-form-item label="焦虑情绪" class="item">
        <Field name="anxiety" v-slot="{ field }">
          <el-switch v-bind="field" v-model="field.value" />
        </Field>
        <div class="msg"><ErrorMessage name="anxiety" /></div>
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

const schemaDisease = readonly(yup.object({
  chronic: yup.boolean().required().default(false),
  allergy: yup.boolean().required().default(false),
  anxiety: yup.boolean().required().default(false)
}))

function onSubmit(values) {
  console.log('提交数据', values);
  emit('submit', values);
}

function onSubmitDisease(values) {
  console.log('疾病史数据', values);
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