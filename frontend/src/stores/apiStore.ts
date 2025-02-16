import { defineStore } from "pinia";
import axios from "axios";
import filePath from "@/helpers/filePath.ts";

const apiPath = filePath.httpClient();

const Authorization =
    "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE3Mzk3MjkzMDd9.P-tAbfOSoQcfoIxj5mYcW86JlK36TiiTSIbFPE9JaIM";

const instance = axios.create({
    baseURL: apiPath,
    headers: {
        Authorization,
    },
});

export const useApiStore = defineStore("apiStore", {
    state: () => ({
        loading: false,
        error: null,
        api: instance,
    }),

    actions: {
        async getData(url: string) {
            this.loading = true;
            this.error = null;

            try {
                const response = await instance.get(`${url}`);
                return response.data;
            } catch (err) {
                this.error = err.response?.data || err.message;
                throw err;
            } finally {
                this.loading = false;
            }
        },

        async postData(url: string, data = {}) {
            this.loading = true;
            this.error = null;
            try {
                const response = await instance.post(`${url}`, data);
                return response.data;
            } catch (err) {
                this.error = err.response?.data || err.message;
                throw err;
            } finally {
                this.loading = false;
            }
        },

        async putData(url: string, data = {}) {
            this.loading = true;
            this.error = null;
            try {
                const response = await instance.put(`${url}`, data);
                return response.data;
            } catch (err) {
                this.error = err.response?.data || err.message;
                throw err;
            } finally {
                this.loading = false;
            }
        },

        async deleteData(url: string) {
            this.loading = true;
            this.error = null;
            try {
                const response = await instance.delete(`${url}`);
                return response.data;
            } catch (err) {
                this.error = err.response?.data || err.message;
                throw err;
            } finally {
                this.loading = false;
            }
        },
    },
});
