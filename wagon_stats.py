import numpy as np
import pandas as pd

from pandas import DataFrame as df

from classifier import TrainPhotosClassifier


def count_wagons(result):
    result_vector = _vectorize(result)

    thunder = 1
    wagon_count = 0

    for previous_image, image in zip(result_vector, result_vector[1:]):
        if previous_image != image and previous_image == thunder:
            wagon_count += 1

    return wagon_count - 1  # without the locomotive


def _vectorize(result):
    vector = result[:, 0]
    vector[vector >= 0.5] = 1
    vector[vector < 0.5] = 0

    return vector.astype('int8')


def split_wagons(result):
    result_vector = _vectorize(result)

    thunder = 1
    wagons = []
    start_new_wagon = True

    for index, image in np.ndenumerate(result_vector):
        if image == thunder:
            start_new_wagon = True
            continue

        if start_new_wagon:
            wagons.append([])

        wagons[-1].append(index[0])
        start_new_wagon = False

    mean_wagon_length = sum([len(wagon) for wagon in wagons])/len(wagons)

    reasonable_size_wagons = []

    for index, wagon in enumerate(wagons): # todo: split too long wagons in half
        wagon_length = len(wagon)

        if wagon_length <= 2:
            continue

        if wagon_length > 1.5 * mean_wagon_length:
            half_a_wagon_len = wagon_length // 2
            reasonable_size_wagons.append(wagon[:half_a_wagon_len])
            reasonable_size_wagons.append(wagon[half_a_wagon_len:])
            continue

        reasonable_size_wagons.append(wagon)

    return reasonable_size_wagons[1:] # the first one is the locomotive


def get_number_of_photos_in_train(result):
    return result.shape[0]


COLUMNS = ['team_name', 'train_number', 'left_right', 'frame_number', 'wagon', 'uic_0_1', 'uic_label']
PATH_TO_WRITE_CSV = '/home/natalia/Projects/queueing/queueing.csv'


def run(train_number):
    dir_path = '/home/natalia/Downloads/cropped_training'
    c = TrainPhotosClassifier(dir_path, train_number)
    result = c.classify_images()

    return split_wagons(result)


def get_csv_data():
    wagons_data = run(0)

    output = df()

    previous_wagon_last_frame = wagons_data[0][0] - 1

    for wagon_number in range(len(wagons_data)):
        for frame_number in range(previous_wagon_last_frame, wagons_data[wagon_number][-1] + 1):
            if wagon_number == 0:
                row_data = ['Queueing', 0, 'left', frame_number, 0, 'locomotive', None]
            else:
                row_data = ['Queueing', 0, 'left', frame_number, 0, wagon_number, None]

            output = pd.concat([output, df([row_data])])

    output['team_name'] = 'Queueing'
    output['train_number'] = 0

    import pdb; pdb.set_trace()

    return output.to_csv(columns=COLUMNS, sep=',', index=False)
