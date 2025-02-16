/** Выравнимание текста */
export type TextAlign = "auto" | "center" | "left" | "right";

interface Sections {
    content?: string;

    /** Выравнимание текста title блока */
    textAlign?: TextAlign;

    /** HEX */
    color?: string;

    /** HEX */
    background?: string;
}

export interface BlockOptions {
    block?: {
        type?: "vertical" | "horizontal";

        /** Выравнимание текста всего блока */
        textAlign?: TextAlign;

        /** 500px = int + "px" */
        maxWidth?: string;
    };

    icon?: {
        name: string;

        /** 70px = int + "px" */
        width: string;
    };

    title?: Sections;
    desc?: Sections;
    text?: Sections;
}
