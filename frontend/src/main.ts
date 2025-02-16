// ------------------------------ SCSS

import "./assets/scss/reset/index.scss";
import "./assets/scss/util/index.scss";

// ------------------------------ Vue

import { createApp } from "vue";
import App from "./App.vue";
const app = createApp(App);

// ------------------------------ Pinia

import { createPinia } from "pinia";
app.use(createPinia());

// ------------------------------ Router

import router from "./router";
app.use(router);

// ------------------------------ ElementPlus

import "element-plus/dist/index.css"; // default CSS
import ElementPlus from "element-plus";
app.use(ElementPlus);

// ------------------------------ mount App

app.mount("#app");
