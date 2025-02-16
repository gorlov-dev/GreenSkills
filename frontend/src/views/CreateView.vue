<script setup lang="ts">
import { ref } from "vue";
import DraggableList from "@/components/DraggableList.vue";

const slideQty = ref(6);
const slideQtyOpt = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

const ratio = ref("2 / 1");
const ratioOpt = [
    {
        label: "2/1",
        value: "2 / 1",
    },
    {
        label: "16/9",
        value: "16 / 9",
    },
];

const lang = ref("ru");
const langOpt = [
    {
        label: "Русский",
        value: "ru",
    },
    {
        label: "Английский",
        value: "en",
    },
];

const search = ref("");

const toolTipData = [
    "Личные финансы",
    "Убедительная презентация",
    "Лекция по экологии коралловых рифов для студентов старших курсов",
    "Раскрывая тайны древних цивилизаций",
    "Предоставление советов и рекомендаций по юридическим",
    "Разработка и реализация контент-стратегии для блога или канала YouTube",
];

const fillData = (text) => {
    search.value = text;
};

const tmpShow = ref(true);

const TableOfContents = ref([
    // {
    //     name: "Joao",
    //     id: 1,
    // },
    // {
    //     name: "Jean",
    //     id: 2,
    // },
    // {
    //     name: "Johanna",
    //     id: 3,
    // },
    // {
    //     name: "Juan",
    //     id: 4,
    // },
]);

const genTableOfContents = () => {
    const endpoint = "presentation/generate";

    if (!search.value) {
        alert("Запрос пуст");
    }

    const payload = {
        prompt: search.value,
        slides_count: slideQty.value,
    };

    apiStore
        .postData(endpoint, payload)
        .then((data) => {
            console.log(data);

            const arr = [];
            data.slides.forEach((el, i) => {
                arr.push({
                    name: el.prompt,
                    id: i + 1,
                });
            });

            TableOfContents.value = arr;

            console.log(arr);

            tmpShow.value = false;
        })
        .catch((err) => {
            alert(err);
        });
};

const theme = ref("Светлая");
const themeOpt = ["Светлая", "Темная"];

const font = ref("Arial");
const fontOpt = ["Arial", "Times New Roman"];

import { useRouter } from "vue-router";
import filePath from "@/helpers/filePath.ts";
const router = useRouter();

import { useApiStore } from "@/stores/apiStore.ts";
const apiStore = useApiStore();

const genPresentation = () => {
    router.push({ name: "edit" });
};
</script>

<template>
    <div class="flex justify-center items-center h-screen">
        <div class="text-center">
            <img :src="filePath.img('ai', 'png')" alt="ai" width="50" class="inline-block mb-5" />

            <div v-if="tmpShow">
                <h1 style="text-transform: uppercase">Сгенерировать</h1>
                <h4 class="mt-2 mb-5">Что бы Вы хотели создать сегодня?</h4>
            </div>
            <div v-else>
                <h4 class="mt-2 mb-5" style="text-transform: uppercase">А теперь перейдем к тонким настройкам</h4>
            </div>

            <div class="mt-10">
                <div class="flex justify-center gap-3">
                    <div>
                        <p class="mb-2">Количество слайдов</p>
                        <el-select v-model="slideQty" placeholder="Select" size="large" style="width: 240px">
                            <el-option v-for="item of slideQtyOpt" :key="item" :label="item" :value="item" />
                        </el-select>
                    </div>

                    <div>
                        <p class="mb-2">Соотношение сторон</p>
                        <el-select v-model="ratio" placeholder="Select" size="large" style="width: 240px">
                            <el-option v-for="item in ratioOpt" :key="item.value" :label="item.label" :value="item.value" />
                        </el-select>
                    </div>

                    <div>
                        <p class="mb-2">Язык</p>
                        <el-select v-model="lang" placeholder="Select" size="large" style="width: 240px">
                            <el-option v-for="item in langOpt" :key="item.value" :label="item.label" :value="item.value" />
                        </el-select>
                    </div>
                </div>

                <div class="mt-10" style="position: relative">
                    <span class="clear" v-if="search" @click="fillData('')">✕</span>
                    <el-input v-model="search" size="large" style="width: 745px" placeholder="Опишите, что Вы хотели бы сделать" />
                </div>
            </div>

            <div class="tmp" v-if="tmpShow">
                <div class="mt-8 flex justify-center gap-3">
                    <hr class="line" style="width: 200px" />
                    <span>Примеры запросов</span>
                    <hr class="line" style="width: 200px" />
                </div>

                <div class="flex-col justify-center mt-10">
                    <div class="flex gap-10 justify-center">
                        <div class="block" @click="fillData(toolTipData[0])">{{ toolTipData[0] }}</div>
                        <div class="block" @click="fillData(toolTipData[1])">{{ toolTipData[1] }}</div>
                        <div class="block" @click="fillData(toolTipData[2])">{{ toolTipData[2] }}</div>
                    </div>
                    <div class="flex gap-10 justify-center mt-10">
                        <div class="block" @click="fillData(toolTipData[3])">{{ toolTipData[3] }}</div>
                        <div class="block" @click="fillData(toolTipData[4])">{{ toolTipData[4] }}</div>
                        <div class="block" @click="fillData(toolTipData[5])">{{ toolTipData[5] }}</div>
                    </div>
                </div>

                <div class="my-10">
                    <el-button type="primary" @click="genTableOfContents"> Сгенерировать cодержание слайдов </el-button>
                </div>
            </div>

            <div v-if="!tmpShow" class="mt-10">
                <div>
                    <h3>Содержание слайдов:</h3>
                    <div class="flex justify-center gap-3 mt-5">
                        <DraggableList :arr="TableOfContents" />
                    </div>
                </div>

                <div class="mt-10">
                    <p class="mb-5">Параметры презентации:</p>
                    <div class="flex justify-center gap-3">
                        <div>
                            <p class="mb-2">Тема</p>
                            <el-select v-model="theme" placeholder="Выберете тему" size="large" style="width: 240px">
                                <el-option v-for="item of themeOpt" :key="item" :label="item" :value="item" />
                            </el-select>
                        </div>

                        <div>
                            <p class="mb-2">Шрифт</p>
                            <el-select v-model="font" placeholder="Выберете шрифт" size="large" style="width: 240px">
                                <el-option v-for="item of fontOpt" :key="item" :label="item" :value="item" />
                            </el-select>
                        </div>
                    </div>
                </div>

                <div class="my-10">
                    <el-button type="primary" @click="genPresentation"> Сгенерировать презентацию </el-button>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
body {
    background: linear-gradient(33deg, #f78fad, #fdeb82);
}
</style>

<style scoped>
.line {
    width: 200px;
    height: 0px;
    border: 1px solid rgba(5, 5, 5, 0.2);
    margin-top: 8px;
}

.clear {
    position: absolute;
    z-index: 100;
    right: 15px;
    top: 10px;
    cursor: pointer;
}

.clear:hover {
    color: #4facfe;
}

.block {
    width: 180px;
    background: #ffffff;
    padding: 20px;

    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;

    -webkit-box-shadow: 0px 0px 20px 0px rgba(0, 0, 0, 0.2);
    -moz-box-shadow: 0px 0px 20px 0px rgba(0, 0, 0, 0.2);
    box-shadow: 0px 0px 20px 0px rgba(0, 0, 0, 0.2);

    cursor: pointer;
}

.block:hover {
    background: #fff3b0;

    -webkit-box-shadow: 0px 0px 20px 0px rgba(0, 0, 0, 0.4);
    -moz-box-shadow: 0px 0px 20px 0px rgba(0, 0, 0, 0.4);
    box-shadow: 0px 0px 20px 0px rgba(0, 0, 0, 0.4);
}

.el-divider--horizontal {
    display: inline-block;
}
.el-divider__text {
    background: transparent;
}
</style>
