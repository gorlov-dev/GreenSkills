<template>
    <div class="flex drag_list">
        <ul
            v-draggable="[
                arr,
                {
                    animation: 150,
                    ghostClass: 'ghost',
                    onUpdate,
                    onStart,
                },
            ]"
            class="flex flex-col gap-2 drag_wrap"
        >
            <li
                v-for="(item, index) in arr"
                :key="item.id"
                class="cursor-move drag_el"
                style="position: relative"
                @mouseenter="showPlus = true"
                @mouseleave="showPlus = false"
            >
                <div class="num">{{ index + 1 }}</div>

                <el-input v-model="item.name" style="width: 400px" size="large" placeholder="Название слайда" class="ml-3 mr-3" />

                <el-button plain @click="handleClose(index)"> ✕ </el-button>
            </li>
        </ul>
        <preview-list :list="arr" />
    </div>
</template>

<script setup lang="ts">
import { ref, toRefs } from "vue";
import { vDraggable } from "vue-draggable-plus";

const props = defineProps({
    arr: {
        type: Array,
        default: () => [],
    },
});

const { arr } = toRefs(props);

import { ElMessageBox } from "element-plus";

const showPlus = ref(false);

const handlePlusClick = () => {
    alert("Плюсик нажат!");
};

const dialogVisible = ref(false);
const handleClose = (index: number) => {
    // dialogVisible.value = true;

    ElMessageBox.confirm("Удалить слайд?")
        .then(() => {
            arr.value.splice(index, 1);
        })
        .catch(() => {
            // catch error
        });
};

function onStart() {
    console.log("start");
}

function onUpdate() {
    console.log("update");
}
</script>

<style>
.el-input__wrapper {
    box-shadow: transparent;
}
</style>

<style scoped>
.ghost {
    opacity: 0.5;
    background: #c8ebfb;
}
.gap-2 {
    gap: 0.5rem;
}
.cursor-move {
    cursor: move;
}
.drag_el {
    background: #ffffff;
    border-radius: 10px;
    padding-right: 10px;
}
.drag_wrap {
}
.drag_list {
    text-align: start;
}
.num {
    display: inline-block;
    padding: 20px;
    color: hsl(218, 20%, 50%);
    background: hsl(219, 100%, 97%);
    border-radius: 10px;
}
</style>
