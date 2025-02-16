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

const mergeOptions = computed(() => {
    const defaultOptionsClone = { ...defaultOptionsSlide };
    const merge = props.options ? deepMerge(defaultOptionsClone, props.options) : defaultOptionsClone;

    return merge;
});
</script>

<template>
    <Slide>
        <div class="flex flex-col justify-center h-full">
            <div class="flex justify-center">
                <Block block-type="vertical" />
            </div>
            <div class="flex mt-20 justify-center gap-20">
                <Block block-type="horizontal" block-text-align="left" />
                <Block block-type="horizontal" block-text-align="left" />
                <Block block-type="horizontal" block-text-align="left" />
            </div>
        </div>
    </Slide>
    <!--    <Slide :options="mergeOptions.slide">-->
    <!--        <div class="flex flex-col gap-10 h-full justify-center items-start ml-16">-->
    <!--            <Block v-for="(e, i) of mergeOptions.blocks" :key="i + 'slide1'" :options="e" />-->
    <!--        </div>-->
    <!--    </Slide>-->
</template>

<style scoped></style>
