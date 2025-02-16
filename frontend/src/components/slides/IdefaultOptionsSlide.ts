import type { BaseSlideOptions } from "@/components/slides/IBaseSlide.ts";
import type { BlockOptions } from "@/components/blocks/IBlock.ts";

export interface DefaultOptionsSlide {
    promt: string | null;
    template: number | null;

    slide: BaseSlideOptions;
    blocks: BlockOptions[];
}
