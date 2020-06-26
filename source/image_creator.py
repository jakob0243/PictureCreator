"""
image_creator.py
Script for creating an image made up of pokemon.

@author Jakob McKinney
"""
import json
import math
import time
from concurrent import futures

import cv2
import numpy as np


def load_data():
    with open("colour_data.json", 'r') as data_set:
        return json.loads(data_set.read())


IMAGE_DICT = load_data()
BACKGROUND_COLOUR = "black"
BACKGROUND_IMAGE_PATH = "./DataSets/Images/24-17.png"
SOURCE_IMG_PATH = "Z:\\new_folder\\GitHub\\PictureCreator\\source\\DataSets\\Images"
FINAL_IMG_PATH = "Z:\\new_folder\\GitHub\\PictureCreator\\source\\DataSets\\Finished"
IMAGES_USED = {}


def rotate_image(image, angle):
    row, col, _ = image.shape
    center = tuple(np.array([row, col])/2)
    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
    new_image = cv2.warpAffine(image, rot_mat, (col, row))

    return new_image


def find_nearest_colour(bgr_colour):
    """
    Iterates over list of images and finds the one closest
    to the given colour.

    @param bgr_colour green, blue, red colour
    """
    min_colour_key = float('inf')
    min_d = float('inf')
    # If the given colour is black then return black as this will be background
    if sum(bgr_colour) == 0:
        min_colour_key = BACKGROUND_COLOUR
        min_d = -1

    for img_name, colour in IMAGE_DICT.items():
        # dif vector of blue components ** 2, + dif vector of green components ** 2, + dif vector of red components ** 2
        # Each colour has vector has a box where the diagonal is the vector and the sides are the r, g  and b components
        # below calculates the difference between these 2 boxes using 3-d pythagoras.
        d = math.sqrt((colour[0] - bgr_colour[0]) ** 2
                      + (colour[1] - bgr_colour[1]) ** 2
                      + (colour[2] - bgr_colour[2]) ** 2)
        if d < min_d:
            min_d = d
            min_colour_key = img_name

    return min_colour_key


def add_to_image(img_array, new_image_name, column):
    """
    Add pixel_img to the img array.

    @param img_array the image being created
    @param new_image_name name of the image to be added
    @param column the current column in the original image
    @return the new image with the image created
    """
    if new_image_name not in IMAGES_USED.keys():
        pixel_img = cv2.imread(SOURCE_IMG_PATH + f"\\{new_image_name}")
        IMAGES_USED[new_image_name] = pixel_img.copy()
    else:
        pixel_img = IMAGES_USED[new_image_name].copy()


    row_nu = 0
    col_nu = column * 80
    for pixel_row in pixel_img:
        for pix in pixel_row:
            if sum(pix) != 0:
                img_array[row_nu][col_nu] = pix
            col_nu += 1
        col_nu = column * 80
        row_nu += 1

    return img_array


def fill_row(row_tup):
    """
    Creates a new 80 by (80*len(row)) image where every pixel in the original row passed in
    is replaced with a 80 by 80 image whose average colour is nearest to the colour of the pixel.

    @param row_tup a tuple containing the row number and the actual row image
    @return row_img an 80 by (80*len(row)) numpy array containing the new image
    """
    row_num = row_tup[0]
    row = row_tup[1]
    print(f"Working on row: {row_num}...")

    row_img = np.zeros((80, 80*len(row), 3), np.uint8)

    current_col = 0
    for pixel in row:  # Iterate over each pixel in the given row
        picture_for_pixel = find_nearest_colour(pixel)
        if picture_for_pixel != BACKGROUND_COLOUR:
            add_to_image(row_img, picture_for_pixel, current_col)
        current_col += 1
    print(f"Row {row_num} completed!")

    return row_img


def create_img(img_path):
    """
    Asynchronously creates a (80 * n) by (80 * n) image for a n by n image given by the passed in img_path.
    The final image is then saved to ./DataSets/Finished folder.

    @param img_path the path of the image to be created
    """
    img = cv2.imread(img_path)
    if img.shape[0] != 80 or img.shape[1] != 80:
        img = cv2.resize(img, (240, 240))

    first = True
    final_img = None
    with futures.ProcessPoolExecutor() as executor:
        for new_row in executor.map(fill_row, enumerate(img)):
            if first:
                final_img = new_row
                first = False
            else:
                final_img = np.concatenate((final_img, new_row))

    img_name = img_path.split('\\')[-1]  # Get image name from the image path
    cv2.imwrite(FINAL_IMG_PATH + f"\\{img_name}", final_img)  # Write created image to FINAL_IMAGE_PATH
    print("Image completed!")


if __name__ == "__main__":
    names = ["16-17"]
    for name in names:
        path = f".\\DataSets\\Images\\{name}.png"
        t_start = time.time()
        create_img(path)
        t_end = time.time()
        print(f"Time taken: {t_end - t_start}")
