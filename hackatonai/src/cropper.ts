import * as rootFs from "fs";
const gm = require("gm").subClass({ imageMagick: true });
const fs = rootFs.promises;
const args = process.argv.slice(2);
const rootTrainingPath = args[0];
const rootSavingPath = args[1];
const top = args[2];
const left = args[3];
const resolution = args[4];

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
                    .crop(
                        Number(resolution),
                        Number(resolution),
                        Number(left),
                        Number(top)
                    )
                    .write(`${savingFilePath}/${filePath}`, () => {
                        console.log(`${savingFilePath}/${filePath}`);
                    });
            }
        }
    }
})();
