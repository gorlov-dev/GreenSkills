<script setup lang="ts">
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import {useAuthStore} from "@/stores/user.ts";

const form = ref({
    identity: '',
    password: ''
});

const authStore = useAuthStore();

const rules = {
    identity: [
        { required: true, message: 'Введите имя пользователя', trigger: 'blur' }
    ],
    password: [
        { required: true, message: 'Введите пароль', trigger: 'blur' }
    ]
};

const formRef = ref<HTMLFormElement>(null);

const onSubmit = () => {
    formRef.value.validate((valid) => {
        if (valid) {
            authStore.login(form.value);
        } else {
            ElMessage.error('Ошибка авторизации');
        }
    });
};
</script>

<template>
    <div class="login-container">
        <el-card class="login-card">
            <h2 class="title">Вход</h2>
            <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
                <el-form-item label="Логин" prop="username">
                    <el-input v-model="form.identity" placeholder="Введите логин" />
                </el-form-item>

                <el-form-item label="Пароль" prop="password">
                    <el-input v-model="form.password" type="password" show-password placeholder="Введите пароль" />
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" @click="onSubmit">Войти</el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<style scoped>
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f5f5f5;
}

.login-card {
    width: 400px;
    padding: 20px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.title {
    text-align: center;
    margin-bottom: 20px;
}
</style>
