"""

@author Jakob McKinney
"""
import json
import math
import time

import cv2
import numpy as np


def load_data():
    """
    Loads in json of the data set

    @return dictionary where key is img name and value is bgr colour
    """
    with open("colour_data.json", 'r') as data_set:
        return json.loads(data_set.read())


IMAGE_DICT = load_data()
BACKGROUND_COLOUR = "black"
BACKGROUND_IMAGE_PATH = "./DataSets/Images/24-17.png"


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

    for name, colour in IMAGE_DICT.items():
        # dif vector of blue components ** 2, + dif vector of green components ** 2, + dif vector of red components ** 2
        # Each colour has vector has a box where the diagonal is the vector and the sides are the r, g  and b components
        # below calculates the difference between these 2 boxes using 3-d pythagoras.
        d = math.sqrt(((colour[0]-bgr_colour[0])*0.3) ** 2
                      + ((colour[1]-bgr_colour[1])*0.59) ** 2
                      + ((colour[2]-bgr_colour[2])*0.11) ** 2)
        if d < min_d:
            min_d = d
            min_colour_key = name

    return min_colour_key


def create_img(img_path):
    """
    Create 6400 * 6400 pixel black image as numpy array then iterate over each pixel
    in original image and a full image for it in the 6400 * 6400 array. Then save full
    array as PNG.
    Currently hard coded size as 80*80 change later

    @param img_path the path of the image to be created
    """
    new_image = np.zeros((6400, 6400, 3), np.uint8)
    img = cv2.imread(img_path)
    cv2.imshow("Diagla", img)
    cv2.waitKey(0)

    current_row = 0
    current_col = 0
    for row in img:  # Iterate over image to create
        for pixel in row:  # Iterate over each pixel in that row
            picture_for_pixel = find_nearest_colour(pixel)
            if picture_for_pixel != BACKGROUND_COLOUR:
                pixel_img = cv2.imread(f"./DataSets/Images/{picture_for_pixel}")
                row_num = current_row * 80
                col_num = current_col * 80
                for pixel_row in pixel_img:
                    for pix in pixel_row:
                        if sum(pix) != 0:
                            new_image[row_num][col_num] = pix
                        col_num += 1
                    col_num = current_col * 80
                    row_num += 1
            current_col += 1
        current_col = 0
        current_row += 1
        print(f"Working on row: {current_row}...")
        print(f"Row {current_row} completed!")
    cv2.imwrite(f"./DataSets/Finished/{img_path[18:]}", new_image)
    print("Image completed!")


if __name__ == "__main__":
    # nearest_value = find_nearest_colour([255, 255, 100])
    # print(f"Name: {nearest_value}, Value: {IMAGE_DICT[nearest_value]}")

    # create_img("./DataSets/Images/6-17.png")
    # create_test()
    start = time.time()
    create_img("./DataSets/Images/0-0.png")
    end = time.time()
    print(f"{end - start} seconds to execute")
    """
    Time before optimisations: 115.4655818939209 seconds to execute on raquaza
    Time after optimisations:
    """
