export type ImgFileExtansion = "svg" | "png" | "jpg";

class FilePath {
    constructor() {
        this.rootPath = "/src";

        this.assetPath = this.rootPath + "/assets";

        this.imgPath = this.assetPath + "/img";
    }

    img(fileName: string = "vue", fileExtansion: ImgFileExtansion = "svg") {
        return this.imgPath + "/" + fileName + "." + fileExtansion;
    }

    httpClient() {
        return "http://91.236.197.135/api/v1/";
    }
}

const filePath = new FilePath();

export default filePath;
