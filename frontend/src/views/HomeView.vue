<script setup lang="ts">
import { ref } from "vue";

import WelcomeBtn from "@/components/WelcomeBtn.vue";

const showButton = ref(true);
const showNewElement = ref(false);

import { useRouter } from "vue-router";
const router = useRouter();

const handleClick = () => {
    showButton.value = false;
    // Запускаем появление нового элемента после завершения анимации исчезновения
    setTimeout(() => {
        showNewElement.value = true;

        router.push({ name: "create" });
    }, 500);
};
</script>

<template>
    <div class="body">
        <!-- Анимация исчезновения кнопки -->
        <transition name="fade">
            <welcome-btn v-if="showButton" class="btn" @click="handleClick" />
        </transition>

        <!-- Анимация появления нового элемента -->
        <transition name="fade"></transition>
    </div>
</template>

<style>
.body {
    width: 100vw;
    height: 100vh;
    background: linear-gradient(33deg, #f78fad, #fdeb82);
}
</style>

<style scoped>
.btn {
    padding: 12px 24px;
    font-size: 18px;
    cursor: pointer;
    border: none;
    color: #fff;
    transition: background 0.3s;
}

/* Анимация плавного исчезновения и появления */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s ease;
}

.fade-enter,
.fade-leave-to {
    opacity: 0;
}
</style>
