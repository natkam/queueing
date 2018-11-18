import os
import sys

import pandas as pd
import pytesseract
from PIL import Image
from tqdm import tqdm


directory_path = sys.argv[-2]
to_directory = sys.argv[-1]


class Klassen:
    @staticmethod
    def get_image(filename):
        BOX = (0, 0, 1180, 900)
        im = Image.open(filename).convert('LA')
        return im.crop(BOX)

    def _get_image_filenames(self, path):
        return [os.path.join(path, filename) for filename in os.listdir(path)]

    def _get_examined_text(self, image_filenames):
        return [pytesseract.image_to_string(self.get_image(filename)) for filename in tqdm(image_filenames)]

    def execute(self, path):
        image_filenames = self._get_image_filenames(path)
        return {
            'filename': image_filenames,
            'text': self._get_examined_text(image_filenames)
        }

csv = Klassen().execute(directory_path)
pd.DataFrame(csv).to_csv(os.path.join(to_directory, 'out.csv'), index=False)
