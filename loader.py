from functools import partial

import numpy as np
from PIL import Image
from sklearn.utils import shuffle
import pathlib


CURRENT_DIR = pathlib.Path(__file__).parent

THUNDER_DIRECTORY_PATH = CURRENT_DIR / 'thunder'
WAGON_DIRECTORY_PATH = CURRENT_DIR / 'wagon'
UIC_DIRECTORY_PATH = CURRENT_DIR / 'UIC'
NONUIC_DIRECTORY_PATH = CURRENT_DIR / 'nonUIC'


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
    get_uic = staticmethod(partial(get_, UIC_DIRECTORY_PATH))
    get_nonuic = staticmethod(partial(get_, NONUIC_DIRECTORY_PATH))


def prepare_uic_data():
    uic = Loader.get_uic()
    nonuic = Loader.get_nonuic()

    X = np.vstack((
        uic,
        nonuic,
    ))

    Y = np.array(
        [[1, 0]]*len(uic) + [[0, 1]]*len(nonuic)
    )

    X = X.astype('float32') / 255
    Y = Y.astype('float32')

    return shuffle(X, Y)


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

    X = X.astype('float32') / 255
    Y = Y.astype('float32')

    return shuffle(X, Y)
