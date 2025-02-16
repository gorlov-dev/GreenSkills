import type { ImgFileExtansion } from "@/helpers/filePath.ts";

interface CornersBlock {
    content: string;

    /** #1a1a1a */
    background: string;

    /** #1a1a1a */
    color?: string;
}

export interface BaseSlideOptions {
    /** 1000px */
    width?: string;

    /** 2/1 */
    ratio?: string;

    /** 40px */
    padding?: string;

    background?: {
        /** #1a1a1a */
        color?: string;
        imgName?: string;
        imgExt?: ImgFileExtansion;
    };

    /** "1px solid #808080" */
    border?: string;

    /** "20px" */
    borderRadius?: string;

    shadow?: boolean;

    corners?: {
        top?: {
            left?: CornersBlock;
            center?: CornersBlock;
            right?: CornersBlock;
        };
        bottom?: {
            left?: CornersBlock;
            center?: CornersBlock;
            right?: CornersBlock;
        };
    };
}
