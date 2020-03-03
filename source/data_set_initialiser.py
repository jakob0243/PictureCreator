"""
Take a data set of images and assign a colour to each of these images based on average colour in image
and save it as a dictionary or something, mapping colour value to img name.

Tasks:
    -   Iterate over directory and load each image into memory then get rid of it, should return list of names
    -   When image is loaded in it avg the colour values of each pixel and map it to the name

@author Jakob McKinney
"""
import sys
import cv2
import numpy


def init_data_set():
    """
    Reads image, splits it up into individual images and saves them
    """
    img = cv2.imread("./DataSets/dataset_pokemon.png")
    cv2.imshow("Image", img)

    print(img.shape)

    x = 0
    y = 160
    for row in range(0, 26):
        print(f"Start: x, y")
        img = cv2.imread("./DataSets/dataset_pokemon.png")
        for col in range(0, 18):
            cropped_img = img.copy()
            cropped_img = cropped_img[x:x+80, y:y+80]
            cv2.imshow("Cropped Img", cropped_img)
            cv2.imwrite(f"./DataSets/Images/{row}-{col}.png", cropped_img)
            x += 80
            print(x, y)
        x = 0
        y += 80
        print(y)

    cv2.destroyAllWindows()




if __name__ == "__main__":
    init_data_set()
