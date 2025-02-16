<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";

const sections = ["1", "2", "3", "4", "5", "6"];
const activeIndex = ref(0);

const scrollToSection = (index) => {
    const section = document.getElementById(sections[index]);
    if (section) {
        section.scrollIntoView({ behavior: "smooth", block: "start" });
        activeIndex.value = index;
    }
};

const slideComponent = (num) => {
    return defineAsyncComponent(() => import(`@/components/slides/Slide${num}.vue`));
};
</script>

<template>
    <el-affix :offset="0">
        <div class="header flex justify-center mb-10">
            <button v-for="(section, index) in sections" :key="section" @click="scrollToSection(index)" :class="{ active: activeIndex === index }">
                {{ section }}
            </button>
        </div>
    </el-affix>

    <div class="sections flex flex-col items-center gap-10">
        <div v-for="(section, index) in sections" :id="section" :key="section" class="section">
            <Transition name="fade">
                <div class="content">
                    {{ section }}
                </div>
            </Transition>
        </div>
    </div>
</template>

<style scoped>
button {
    margin: 5px;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    background: #007bff;
    color: #fff;
    transition: background 0.3s;
}

button:hover {
    background: #0056b3;
}

button.active {
    background: #28a745;
}

.sections {
    height: 500vh;
}

.section {
    height: 100vh;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    color: #fff;
    background: #333;
    border-bottom: 1px solid #ccc;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}
.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.header {
    background: #1a1a1a;
    padding: 15px;
}
</style>
