from functools import partial

import numpy as np
from PIL import Image
from sklearn.utils import shuffle
import pathlib


CURRENT_DIR = pathlib.Path(__file__).parent

THUNDER_DIRECTORY_PATH = CURRENT_DIR / 'thunder'
WAGON_DIRECTORY_PATH = CURRENT_DIR / 'wagon'


class Loader:

    def get_(DIR_PATH):
        img_array = []

        for img_path in pathlib.Path(DIR_PATH).iterdir():
            img = Image.open(img_path)

            img_np = np.array(img)
            img_array.append(np.array([img_np]))

        return np.vstack(img_array)

    get_thunders = staticmethod(partial(get_, THUNDER_DIRECTORY_PATH))
    get_wagons = staticmethod(partial(get_, WAGON_DIRECTORY_PATH))


def prepare_fit_data():
    thunders = Loader.get_thunders()
    wagons = Loader.get_wagons()

    X = np.vstack((
        thunders,
        wagons
    ))

    Y = np.array(
        [[1, 0]]*len(thunders) + [[0, 1]]*len(wagons)
    )

    return shuffle(X, Y)
