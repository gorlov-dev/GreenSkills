<script setup lang="ts">
import { computed, ref } from "vue";
import deepMerge from "@/helpers/deepMerge.ts";
import filePath from "@/helpers/filePath.ts";
import type { BaseSlideOptions } from "@/components/slides/IBaseSlide.ts";

const props = defineProps({
    options: {
        type: Object,
    },
});

const defaultOptions: BaseSlideOptions = {
    width: "1000px",
    // width: "100%",
    ratio: "2/1",

    padding: "40px",

    background: {
        color: "#1a1a1a",
        imgName: "bg1",
    },

    border: "1px solid #808080",
    borderRadius: "20px",
    shadow: true,

    // img

    corners: {
        top: {
            left: "left",
            center: "center",
            right: "right",
        },
        bottom: {
            left: "left",
            center: "center",
            right: "right",
        },
    },
};

const mergeOptions = computed(() => {
    const defaultOptionsClone = { ...defaultOptions };
    const merge = props.options ? deepMerge(defaultOptionsClone, props.options) : defaultOptionsClone;

    if (merge.background.color) {
        merge.background = merge.background.color;
    } else if (merge.background.imgName) {
        const path = filePath.img(merge.background.imgName, merge.background.imgExt || "png");
        merge.background = `url("${path}")`;
    }

    return merge;
});

import { useBaseStore } from "@/stores/base.store.ts";
const baseStore = useBaseStore();
const editMode = computed(() => baseStore.editMode);
</script>

<template>
    <div class="slide">
        <div class="promtName">{{ mergeOptions.promt }} Текст промпта</div>
        <div class="numSlide">1</div>

        <div class="corner top-20">
            <div class="corner-top-left">
                <div v-if="!editMode">
                    {{ mergeOptions.corners.top.left.content }}
                </div>
                <div class="flex" v-else>
                    <el-input v-model="mergeOptions.corners.top.left.content" />
                    <div class="flex ml-2">
                        <el-color-picker v-model="mergeOptions.corners.bottom.right.color" />
                        <el-color-picker v-model="mergeOptions.corners.bottom.right.background" />
                    </div>
                </div>
            </div>
            <div class="corner-top-center">
                <div v-if="!editMode">
                    {{ mergeOptions.corners.top.center.content }}
                </div>
                <div class="flex" v-else>
                    <el-input v-model="mergeOptions.corners.top.center.content" />
                    <div class="flex ml-2">
                        <el-color-picker v-model="mergeOptions.corners.bottom.right.color" />
                        <el-color-picker v-model="mergeOptions.corners.bottom.right.background" />
                    </div>
                </div>
            </div>
            <div class="corner-top-right">
                <div v-if="!editMode">
                    {{ mergeOptions.corners.top.right.content }}
                </div>
                <div class="flex" v-else>
                    <el-input v-model="mergeOptions.corners.top.right.content" />
                    <div class="flex ml-2">
                        <el-color-picker v-model="mergeOptions.corners.bottom.right.color" />
                        <el-color-picker v-model="mergeOptions.corners.bottom.right.background" />
                    </div>
                </div>
            </div>
        </div>

        <slot></slot>

        <div class="corner bottom-20">
            <div class="corner-bottom-left">
                <div v-if="!editMode">
                    {{ mergeOptions.corners.bottom.left.content }}
                </div>
                <div class="flex" v-else>
                    <el-input v-model="mergeOptions.corners.bottom.left.content" />
                    <div class="flex ml-2">
                        <el-color-picker v-model="mergeOptions.corners.bottom.right.color" />
                        <el-color-picker v-model="mergeOptions.corners.bottom.right.background" />
                    </div>
                </div>
            </div>
            <div class="corner-bottom-center">
                <div v-if="!editMode">
                    {{ mergeOptions.corners.bottom.center.content }}
                </div>
                <div class="flex" v-else>
                    <el-input v-model="mergeOptions.corners.bottom.center.content" />
                    <div class="flex ml-2">
                        <el-color-picker v-model="mergeOptions.corners.bottom.right.color" />
                        <el-color-picker v-model="mergeOptions.corners.bottom.right.background" />
                    </div>
                </div>
            </div>
            <div class="corner-bottom-right">
                <div v-if="!editMode">
                    {{ mergeOptions.corners.bottom.right.content }}
                </div>
                <div class="flex" v-else>
                    <el-input v-model="mergeOptions.corners.bottom.right.content" />
                    <div class="flex ml-2">
                        <el-color-picker v-model="mergeOptions.corners.bottom.right.color" />
                        <el-color-picker v-model="mergeOptions.corners.bottom.right.background" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.el-color-picker__trigger {
    border: 1px solid transparent;
}

.el-input__wrapper {
    background-color: transparent;
    box-shadow: none;
}
.el-input__inner {
    color: #fff;
}
</style>

<style scoped lang="scss">
.promtName {
    position: absolute;
    top: -25px;
}
.numSlide {
    position: absolute;
    top: 50%;
    left: -100px;
    background: #4facfe;
    color: #fff;
    padding: 20px;
    border-radius: 10px;
    font-weight: bold;
}
.corner-top-left {
    color: #2ecc71;
    background: #636865;
}

.corner-top-center {
    color: #2ecc71;
    background: #636865;
}

.corner-top-right {
    color: #2ecc71;
    background: #636865;
}

.corner-bottom-left {
    color: #2ecc71;
    background: #636865;
}

.corner-bottom-center {
    color: #2ecc71;
    background: #636865;
}

.corner-bottom-right {
    color: #2ecc71;
    background: #636865;
}

.slide {
    position: relative;

    width: v-bind("mergeOptions.width");
    aspect-ratio: v-bind("mergeOptions.ratio");
    padding: v-bind("mergeOptions.padding");

    border: 1px solid #808080;
    border-radius: 20px;

    background: v-bind("mergeOptions.background");

    -webkit-box-shadow: 0px 0px 20px 0px rgba(179, 179, 179, 0.2);
    -moz-box-shadow: 0px 0px 20px 0px rgba(179, 179, 179, 0.2);
    box-shadow: 0px 0px 20px 0px rgba(179, 179, 179, 0.2);

    .corner {
        display: flex;
        justify-content: space-between;
        position: absolute;
        width: inherit;

        & > div {
            padding: 5px 10px;
        }
    }
}
</style>
