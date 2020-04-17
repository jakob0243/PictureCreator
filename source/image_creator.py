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

    for name, colour in IMAGE_DICT.items():
        # dif vector of blue components ** 2, + dif vector of green components ** 2, + dif vector of red components ** 2
        # Each colour has vector has a box where the diagonal is the vector and the sides are the r, g  and b components
        # below calculates the difference between these 2 boxes using 3-d pythagoras.
        """d = math.sqrt(((colour[0]-bgr_colour[0])*0.3) ** 2
                      + ((colour[1]-bgr_colour[1])*0.59) ** 2
                      + ((colour[2]-bgr_colour[2])*0.11) ** 2)"""
        d = math.sqrt((colour[0] - bgr_colour[0]) ** 2
                      + (colour[1] - bgr_colour[1]) ** 2
                      + (colour[2] - bgr_colour[2]) ** 2)
        if d < min_d:
            min_d = d
            min_colour_key = name

    return min_colour_key


def add_to_image(img_array, new_image_name, column, row):
    """
    Add pixel_img to the img array.

    @param img_array the image being created
    @param new_image_name name of the image to be added
    @param column the current column in the original image
    @param row the current row in the original image
    @return the new image with the image created
    """
    if new_image_name not in IMAGES_USED.keys():
        pixel_img = cv2.imread(f"./DataSets/Images/{new_image_name}")
        IMAGES_USED[new_image_name] = pixel_img.copy()
    else:
        pixel_img = IMAGES_USED[new_image_name].copy()


    row_nu = row * 80
    col_nu = column * 80
    for pixel_row in pixel_img:
        for pix in pixel_row:
            if sum(pix) != 0:
                img_array[row_nu][col_nu] = pix
            col_nu += 1
        col_nu = column * 80
        row_nu += 1

    return img_array


def create_img(img_path):
    """
    Create 6400 * 6400 pixel black image as numpy array then iterate over each pixel
    in original image and a full image for it in the 6400 * 6400 array. Then save full
    array as PNG.
    Currently hard coded size as 80*80 change later

    @param img_path the path of the image to be created
    """
    img = cv2.imread(img_path)
    if img.shape[0] != 80 or img.shape[1] != 80:
        img = cv2.resize(img, (240, 240))
    new_image = np.zeros((80*img.shape[0], 80*img.shape[1], 3), np.uint8)

    # cv2.imshow(img_path[18:], img)
    # cv2.waitKey(0)
    # Rotate and flip, solves weird bug where created image is flipped and rotated
    img = cv2.flip(rotate_image(img, 270), 1)

    current_row = 0
    current_col = 0
    for row in img:  # Iterate over image to create
        for pixel in row:  # Iterate over each pixel in that row
            picture_for_pixel = find_nearest_colour(pixel)
            if picture_for_pixel != BACKGROUND_COLOUR:
                new_image = add_to_image(new_image, picture_for_pixel, current_row, current_col)
            current_col += 1
        current_col = 0
        current_row += 1
        print(f"Working on row: {current_row}...")
        print(f"Row {current_row} completed!")

    cv2.imwrite(f"./DataSets/Finished/Test{img_path[18:]}", new_image)  #rotate_image(new_image, 270))  # {img_path[18:]}", new_image) flip 0
    print("Image completed!")


if __name__ == "__main__":
    # nearest_value = find_nearest_colour([255, 255, 100])
    # print(f"Name: {nearest_value}, Value: {IMAGE_DICT[nearest_value]}")

    # create_img("./DataSets/Images/6-17.png")
    # create_test()
    """
    img_path = "./DataSets/Images/19-13.png"
    start = time.time()
    create_img(img_path)
    end = time.time()
    print(f"{end - start} seconds to execute")
    """
    names = ["Tess"]  # ["18-8", "19-8", "20-8", "14-17", "9-17", "7-17", "3-5", "4-5", "5-5"]
    for name in names:
        img_path = f"./DataSets/Images/{name}.png"
        create_img(img_path)
    """
    Time before optimisations: 115.4655818939209 seconds to execute on raquaza
    Time after adding IMAGES_USED dict: 112.70291018486023
    
    TODO: make sure it is made correctly so don't need to flip and pics will be correct orientation
    """
    # cv2.imwrite("./DataSets/Finished/Test.png", cv2.flip(read, 0))
    # read = cv2.imread("./DataSets/Finished/Test.png")
    # cv2.imwrite("./DataSets/Finished/Test.png", rotate_image(read, 270))
    # read = cv2.imread(f"./DataSets/Finished/Test{img_path[18:]}")
    # cv2.imwrite(f"./DataSets/Finished/Test{img_path[18:]}", cv2.flip(read, 1))
    # image = cv2.imread("./DataSets/pokeballtest.jfif")
    # image = cv2.resize(image, (80, 80))
    # cv2.imwrite("./DataSets/pokeball.png", image)
