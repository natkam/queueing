import os
import sys
import pathlib

from PIL import Image

CROP_BOX = (639, 421, 639+100, 421+100)

directory_path = sys.argv[-2]
to_directory = sys.argv[-1]

for path in os.listdir(directory_path):
    image_path = pathlib.Path(directory_path, path)
    image_name = image_path.name

    img = Image.open(image_path)

    thunder_image = img.crop(CROP_BOX)
    thunder_image.save(os.path.join(to_directory, image_name))
