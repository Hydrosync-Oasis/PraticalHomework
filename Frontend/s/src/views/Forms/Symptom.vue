<template>
    <Form :validation-schema="schemaSymptom" v-slot="{ handleSubmit }" :initial-values="{
        yellow_fingers: false,
        fatigue: false,
        wheezing: false,
        coughing: false,
        shortness_of_breath: false,
        swallowing_difficulty: false,
        chest_pain: false
    }">
        <el-form class="form" @submit.prevent="handleSubmit(onSubmitSymptom)">
            <el-form-item label="黄手指" class="item">
                <Field name="yellow_fingers" v-slot="{ field }">
                    <el-switch v-bind="field" v-model="field.value" />
                </Field>
                <div class="msg">
                    <ErrorMessage name="yellowFingers" />
                </div>
            </el-form-item>

            <el-form-item label="疲劳感" class="item">
                <Field name="fatigue" v-slot="{ field }">
                    <el-switch v-bind="field" v-model="field.value" />
                </Field>
                <div class="msg">
                    <ErrorMessage name="fatigue" />
                </div>
            </el-form-item>

            <el-form-item label="喘息" class="item">
                <Field name="wheezing" v-slot="{ field }">
                    <el-switch v-bind="field" v-model="field.value" />
                </Field>
                <div class="msg">
                    <ErrorMessage name="wheezing" />
                </div>
            </el-form-item>

            <el-form-item label="咳嗽" class="item">
                <Field name="coughing" v-slot="{ field }">
                    <el-switch v-bind="field" v-model="field.value" />
                </Field>
                <div class="msg">
                    <ErrorMessage name="coughing" />
                </div>
            </el-form-item>

            <el-form-item label="呼吸急促" class="item">
                <Field name="shortness_of_breath" v-slot="{ field }">
                    <el-switch v-bind="field" v-model="field.value" />
                </Field>
                <div class="msg">
                    <ErrorMessage name="shortnessOfBreath" />
                </div>
            </el-form-item>

            <el-form-item label="吞咽困难" class="item">
                <Field name="swallowing_difficulty" v-slot="{ field }">
                    <el-switch v-bind="field" v-model="field.value" />
                </Field>
                <div class="msg">
                    <ErrorMessage name="swallowingDifficulty" />
                </div>
            </el-form-item>

            <el-form-item label="胸痛" class="item">
                <Field name="chest_pain" v-slot="{ field }">
                    <el-switch v-bind="field" v-model="field.value" />
                </Field>
                <div class="msg">
                    <ErrorMessage name="chestPain" />
                </div>
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

const schemaSymptom = readonly(yup.object({
  yellow_fingers: yup.boolean().required().default(false),
  fatigue: yup.boolean().required().default(false),
  wheezing: yup.boolean().required().default(false),
  coughing: yup.boolean().required().default(false),
  shortness_of_breath: yup.boolean().required().default(false),
  swallowing_difficulty: yup.boolean().required().default(false),
  chest_pain: yup.boolean().required().default(false)
}))

function onSubmitSymptom(values) {
  console.log('症状数据', values);
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