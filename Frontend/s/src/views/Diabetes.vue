<template>
    <el-container>
        <el-header>
            <h1>
                填写题目，获取你的糖尿病患病率：
            </h1>
        </el-header>
        <el-main>
            <el-steps :active="index">
                <el-step title="基本信息" description="年龄与性别"></el-step>
                <el-step title="结果" description="查看预测结果"></el-step>
            </el-steps>

            <div class="form">
                <div v-if="index === components.length - 1">
                    <ResultCard :prediction="result['预测结果']" :prediction-label="result['预测结果']"
                        :probability="result['概率']" style="margin: 20px;">

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
import BasicForm from './Forms/Diabetes/BasicInfo.vue'
import ResultCard from './ResultCard.vue'
import { PredictDiabetes } from '../api/ml.js'
import { reactive, ref } from 'vue'

const components = [BasicForm, ResultCard];
const index = ref(0);
const result = reactive({});

function F(values) {
    index.value++;
    console.log(index.value);

    if (index.value === components.length - 1) {
        // axios
        const data = {};
        Object.assign(data, values);
        
        PredictDiabetes(data).then(
            (res) => {
                Object.assign(result, res.data[0]);
                console.log(result);
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