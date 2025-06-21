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
                <el-step title="结果" description="查看预测结果"></el-step>
            </el-steps>

            <div class="form">
                <div v-if="index === components.length - 1">
                    <ResultCard :prediction="result.prediction" :prediction-label="result['prediction_label']"
                        :probability="result.probability" style="margin: 20px;">

                    </ResultCard>
                </div>
                <div v-else>
                    <component :is="components[index]" @submit="F">
                    </component>
                </div>
            </div>
        </el-main>
    </el-container>
</template>

<script setup>
import BasicForm from './Forms/BasicInfo.vue'
import DiseaseForm from './Forms/Disease.vue'
import SymptomForm from './Forms/Symptom.vue'
import ResultCard from './ResultCard.vue'
import { PredictLungCancer } from '../api/ml.js'
import { reactive, ref } from 'vue'

const components = [BasicForm, DiseaseForm, SymptomForm, ResultCard];
const formsData = [];
const index = ref(0);
const result = reactive({});

function F(values) {
    formsData[index.value] = values;
    index.value++;
    console.log(index.value);

    if (index.value === components.length - 1) {
        // axios
        const data = {};
        Object.assign(data, ...formsData);
        for (let item of Object.keys(data)) {
            if (typeof data[item] === 'boolean') {
                data[item] = data[item] ? 2 : 1;
            }
        }
        PredictLungCancer(data).then(
            (res) => {
                Object.assign(result, res.data);
            }
        );
        return;
    }
}
</script>

<style scoped>
.form {
    width: 30%;
    min-width: 580px;
    margin-top: 30px;
    margin-left: auto;
    margin-right: auto;
    border: 2px gray;
}
</style>