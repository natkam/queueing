import os
import pathlib

import numpy as np
from PIL import Image
from keras.models import load_model

CURRENT_DIR = pathlib.Path(__file__).parent

MODEL_PATH = CURRENT_DIR / 'cnn_tanh_0.97.h5'


class TrainPhotosClassifier:
    """
    :dir_path: str - the directory with all the train folders, without a trailing slash
    :train_number:
    """

    def __init__(self, dir_path, train_number):
        self.dir_path = dir_path
        self.train_number = train_number
        self.inside_dir_path = f'{self.dir_path}/0_{self.train_number}/0_{self.train_number}_left'

    def _load_images(self):
        img_array = []

        image_count = len(os.listdir(self.inside_dir_path))

        for index in range(image_count):
            img_path = f'{self.inside_dir_path}/0_{self.train_number}_left_{index}.jpg'

            try:
                img = Image.open(img_path)
            except FileNotFoundError:
                continue

            img_np = np.array(img)
            img_array.append(np.array([img_np]))

        return np.vstack(img_array).astype('float32') / 255

    def classify_images(self):
        model = load_model(str(MODEL_PATH))
        data = self._load_images()
        result = model.predict(data)

        return result
