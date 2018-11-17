import * as rootFs from "fs";
const gm = require("gm").subClass({ imageMagick: true });
const fs = rootFs.promises;
const args = process.argv.slice(2);
const rootTrainingPath = args[0];
const rootSavingPath = args[1];
const width = args[2];

(async () => {
    const trainDirPath: string[] = await fs.readdir(rootTrainingPath);
    for (const trainDir of trainDirPath) {
        const leftRightDirPath: string[] = (await fs.readdir(
            `${rootTrainingPath}/${trainDir}`
        )).slice(1);
        for (const leftRightDir of leftRightDirPath) {
            const fileDirPath: string[] = await fs.readdir(
                `${rootTrainingPath}/${trainDir}/${leftRightDir}`
            );
            for (const filePath of fileDirPath) {
                const savingFilePath: string = `${rootSavingPath}/${trainDir}/${leftRightDir}`;
                await fs.mkdir(savingFilePath, { recursive: true });
                gm(
                    `${rootTrainingPath}/${trainDir}/${leftRightDir}/${filePath}`
                )
                    .type("grayscale")
                    .resize(Number(width))
                    .write(`${savingFilePath}/${filePath}`, () => {
                        console.log(`${savingFilePath}/${filePath}`);
                    });
            }
        }
    }
})();
