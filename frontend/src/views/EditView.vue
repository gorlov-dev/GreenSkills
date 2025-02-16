<script setup lang="ts">
import { useRouter } from "vue-router";
import { computed, defineAsyncComponent } from "vue";
import { defaultOptionsSlide } from "@/components/slides/defaultOptionsSlide.ts";
import deepMerge from "@/helpers/deepMerge.ts";
const router = useRouter();

const play = () => {
    router.push({ name: "play" });
};

const props = defineProps({
    options: {
        type: Object,
        default: () => ({}),
    },
});

const genMockData = () => {
    const presentation = {
        id: 1,
        slides: [],
    };

    for (let i = 1; i <= 6; i++) {
        const slide = { ...defaultOptionsSlide };
        slide.template = i;
        slide.promt = "дисковая файловая система";
        presentation.slides.push(slide);
    }

    return presentation;
};

const mergeOptions = computed(() => {
    let data = {};
    if (!props.options.slides) data = genMockData();

    // const defaultOptionsClone = ;
    // const merge = props.options ? deepMerge(defaultOptionsClone, props.options) : defaultOptionsClone;

    return data;
});

const slideComponent = (num) => {
    return defineAsyncComponent(() => import(`@/components/slides/Slide${num}.vue`));
};

import { useBaseStore } from "@/stores/base.store.ts";
const baseStore = useBaseStore();
</script>

<template>
    <el-affix :offset="0">
        <div class="header flex justify-center mb-10">
            <el-button type="primary" @click="play">Опубликовать</el-button>
            <div>
                <el-switch class="ml-10" v-model="baseStore.editMode" />
                <span class="ml-2"> Редактирование </span>
            </div>
        </div>
    </el-affix>

    <div class="flex flex-col items-center gap-10">
        <component v-for="e of mergeOptions.slides" :is="slideComponent(e.template)" />
    </div>
</template>

<style scoped>
.header {
    background: #1a1a1a;
    padding: 15px;
}
</style>
