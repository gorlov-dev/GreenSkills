<script setup lang="ts">
import Block from "@/components/blocks/Block.vue";
import Slide from "@/components/slides/BaseSlide.vue";
import { computed } from "vue";
import { defaultOptionsSlide } from "@/components/slides/defaultOptionsSlide.ts";
import deepMerge from "@/helpers/deepMerge.ts";

const props = defineProps({
    options: {
        type: Object,
    },
});

const applyCustomOptions = (defaultOptionsClone: object) => {
    for (const el of defaultOptionsClone.blocks) {
        el.block.type = "vertical";
    }
};

const mergeOptions = computed(() => {
    const defaultOptionsClone = { ...defaultOptionsSlide };
    applyCustomOptions(defaultOptionsClone);

    const merge = props.options ? deepMerge(defaultOptionsClone, props.options) : defaultOptionsClone;

    return merge;
});
</script>

<template>
    <Slide :options="mergeOptions.slide">
        <div class="flex items-center h-full justify-center gap-20">
            <Block v-for="(e, i) of mergeOptions.blocks" :key="i + 'slide1'" :options="e" />
        </div>
    </Slide>
</template>

<style scoped></style>
