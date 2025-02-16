import { defineStore } from "pinia";

import { ref } from "vue";
import { ElMessage } from "element-plus";
import filePath from "@/helpers/filePath.ts";
import axios from "axios";

const apiPath = filePath.httpClient();

const Authorization =
    "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE3Mzk3MjkzMDd9.P-tAbfOSoQcfoIxj5mYcW86JlK36TiiTSIbFPE9JaIM";

const instance = axios.create({
    baseURL: apiPath,
    headers: {
        Authorization,
    },
});

export const useAuthStore = defineStore("auth", () => {
    // State
    const user = ref(null);
    const loading = ref(false);

    // Actions
    const login = async (credentials) => {
        loading.value = true;

        try {
            const response = await instance.post(`auth/login`, credentials);
            user.value = response.data;
            console.log(response.data);
            localStorage.setItem("token", response.data.token);
            axios.defaults.headers.common["Authorization"] = `Bearer ${response.data.token}`;

            ElMessage.success("Вход выполнен успешно");
            return response.data;
        } catch (error) {
            ElMessage.error(error.response?.data?.message || "Ошибка авторизации");
            throw error;
        } finally {
            loading.value = false;
        }
    };

    const logout = () => {
        user.value = null;
        ElMessage.info("Вы вышли из системы");
    };

    return { user, loading, login, logout };
});
