import { createRouter, createWebHistory } from "vue-router";

function isAuthenticated() {
    return !!localStorage.getItem("token");
}

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "authorization",
            component: () => import("@/views/AuthorizationView.vue"),
        },
        {
            path: "/home",
            name: "home",
            component: () => import("@/views/HomeView.vue"),
            meta: { requiresAuth: true },
        },
        {
            path: "/create",
            name: "create",
            component: () => import("@/views/CreateView.vue"),
            meta: { requiresAuth: true },
        },
        {
            path: "/edit",
            name: "edit",
            component: () => import("@/views/EditView.vue"),
            meta: { requiresAuth: true },
        },
        {
            path: "/play",
            name: "play",
            component: () => import("@/views/PlayView.vue"),
            meta: { requiresAuth: true },
        },
    ],
});

router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth && !isAuthenticated()) {
        next("/"); // Перенаправляем на страницу входа
    } else {
        next(); // Продолжаем навигацию
    }
});

export default router;
