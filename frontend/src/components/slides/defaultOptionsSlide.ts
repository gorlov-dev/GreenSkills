import type { DefaultOptionsSlide } from "@/components/slides/IdefaultOptionsSlide.ts";

export const defaultOptionsSlide: DefaultOptionsSlide = {
    promt: "",

    /** номер темплейта */
    template: null,

    slide: {
        background: {
            imgName: "bg1",
        },
        corners: {
            top: {
                left: {
                    content: "Text",
                    color: "#7a6c4e",
                    background: "#6c6969",
                },
                center: {
                    content: "Text",
                    color: "#7a6c4e",
                    background: "#6c6969",
                },
                right: {
                    content: "Text",
                    color: "#7a6c4e",
                    background: "#6c6969",
                },
            },
            bottom: {
                left: {
                    content: "Text",
                    color: "#7a6c4e",
                    background: "#6c6969",
                },
                center: {
                    content: "Text",
                    color: "#7a6c4e",
                    background: "#6c6969",
                },
                right: {
                    content: "Text",
                    color: "#7a6c4e",
                    background: "#6c6969",
                },
            },
        },
    },

    blocks: [
        // --------------------------- block
        {
            block: {
                type: "horizontal",
                textAlign: "left",
            },
            title: {
                content: "Text",
                background: "#6c6969",
            },
            desc: {
                content: "Text",
                background: "#6c6969",
            },
            text: {
                content: "Text",
                background: "#6c6969",
            },
        },
        // --------------------------- block
        {
            block: {
                type: "horizontal",
                textAlign: "left",
            },
            title: {
                content: "Text",
                background: "#6c6969",
            },
            desc: {
                content: "Text",
                background: "#6c6969",
            },
            text: {
                content: "Text",
                background: "#6c6969",
            },
        },
        // --------------------------- block
        {
            block: {
                type: "horizontal",
                textAlign: "left",
            },
            title: {
                content: "Text",
                background: "#6c6969",
            },
            desc: {
                content: "Text",
                background: "#6c6969",
            },
            text: {
                content: "Text",
                background: "#6c6969",
            },
        },
        // ---------------------------
    ],
};
