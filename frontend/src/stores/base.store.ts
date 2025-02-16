import { defineStore } from "pinia";
import { ref } from "vue";

export const useBaseStore = defineStore("base", () => {
    // State
    const editMode = ref(false);

    return { editMode };
});
