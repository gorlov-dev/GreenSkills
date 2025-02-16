<script setup lang="ts">
import { computed } from "vue";
import deepMerge from "@/helpers/deepMerge.ts";
import filePath from "@/helpers/filePath.ts";

import type { BlockOptions } from "@/components/blocks/IBlock.ts";

const defaultOptions: BlockOptions = {
    block: {
        type: "horizontal",
        textAlign: "center",
        maxWidth: "500px",
    },
    icon: {
        name: "vue",
        width: "70px",
    },
    title: {
        content: "",
        textAlign: "auto",
        color: "#EF5350",
        background: "transparent",
    },
    desc: {
        content: "",
        textAlign: "auto",
        color: "#fff",
        background: "transparent",
    },
    text: {
        content: "",
        textAlign: "auto",
        color: "#fff",
        background: "transparent",
    },
};

const props = defineProps({
    // -------------------

    options: {
        type: Object,
    },
});

const mergeOptions = computed(() => {
    const defaultOptionsClone = { ...defaultOptions };
    return props.options ? deepMerge(defaultOptionsClone, props.options) : defaultOptionsClone;
});
</script>

<template>
    <template v-if="mergeOptions.block.type === 'vertical'">
        <div class="block">
            <div v-if="mergeOptions.icon.name" class="icon mb-4">
                <img :src="filePath.img(mergeOptions.icon.name)" :alt="mergeOptions.icon.name" />
            </div>
            <div v-if="mergeOptions.title.content" class="title">
                <h2>{{ mergeOptions.title.content }}</h2>
            </div>
            <div v-if="mergeOptions.descContent" class="desc">
                {{ mergeOptions.desc.content }}
            </div>
            <div v-if="mergeOptions.text.content" class="text mt-2">
                {{ mergeOptions.text.content }}
            </div>
        </div>
    </template>
    <template v-else>
        <div class="block flex items-start">
            <div v-if="mergeOptions.icon.name" class="icon mr-6 mt-2">
                <img :src="filePath.img(mergeOptions.icon.name)" :alt="mergeOptions.icon.name" />
            </div>
            <div>
                <div v-if="mergeOptions.title.content" class="title">
                    <h2>{{ mergeOptions.title.content }}</h2>
                </div>
                <div v-if="mergeOptions.desc.content" class="desc">
                    {{ mergeOptions.desc.content }}
                </div>
                <div v-if="mergeOptions.text.content" class="text mt-4">
                    {{ mergeOptions.text.content }}
                </div>
            </div>
        </div>
    </template>
</template>

<style lang="scss" scoped>
.block {
    max-width: v-bind("mergeOptions.block.maxWidth");
    text-align: v-bind("mergeOptions.block.textAlign");
    // color не добавлять
}
.icon {
    display: inline-block;
    img {
        width: v-bind("mergeOptions.icon.width");
    }
}
.title {
    text-align: v-bind("mergeOptions.title.textAlign");
    color: v-bind("mergeOptions.title.color");
    background: v-bind("mergeOptions.title.background");
    padding: 5px;
}
.desc {
    text-align: v-bind("mergeOptions.desc.textAlign");
    color: v-bind("mergeOptions.desc.color");
    background: v-bind("mergeOptions.title.background");
    padding: 5px;
}
.text {
    text-align: v-bind("mergeOptions.text.textAlign");
    color: v-bind("mergeOptions.text.color");
    background: v-bind("mergeOptions.title.background");
    padding: 5px;
}
</style>
