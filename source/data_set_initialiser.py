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
import json


IMAGE_DIR = "./DataSets/Images/"
IMAGE_HEIGHT = 80
IMAGE_WIDTH = 80


def avg_colour(img):
    """
    Averages the colour of all the pixels in the image.
    Ignores black backgrounds.
    Could average r values then g values then b values and return an actual colour

    @param img an image
    @return the average value of the pixels
    """
    total = 0
    total2 = 0
    total3 = 0
    num_pixels = 0
    for row in img:
        for pixel in row:
            p_sum = sum(pixel)
            # Ignore if it is a black pixel as this is the background colour
            if p_sum > 0:
                total += pixel[0]
                total2 += pixel[1]
                total3 += pixel[2]
                num_pixels += 1

    print(f"Total: {total}")
    print(f"No. pixels: {num_pixels}")
    return [int((total / num_pixels)), int((total2 / num_pixels)), int((total3 / num_pixels))]


def read_images():
    """
    Read images in directory, average the colour for each
    image and save it.
    """
    colour_values = {}

    for row in range(0, 26):
        for col in range(0, 18):
            current_img = f"{row}-{col}.png"
            to_avg = cv2.imread(IMAGE_DIR + current_img)
            # cv2.imshow("image", to_avg)
            # cv2.waitKey(0)
            try:
                colour = avg_colour(to_avg)
                colour_values[current_img] = colour
            except ZeroDivisionError as e:
                print("All black picture found and not counted")


    with open("colour_data.json", "w") as outfile:
        json.dump(colour_values, outfile)



def init_data_set():
    """
    Reads image, splits it up into individual images and saves them
    """
    x = 0
    y = 0
    for row in range(0, 26):
        img = cv2.imread("./DataSets/dataset_pokemon.png")
        for col in range(0, 18):
            cropped_img = img.copy()
            cropped_img = cropped_img[x:x+IMAGE_WIDTH, y:y+IMAGE_HEIGHT]
            cv2.imwrite(f"./DataSets/Images/{row}-{col}.png", cropped_img)
            x += IMAGE_WIDTH
        x = 0
        y += IMAGE_HEIGHT

    cv2.destroyAllWindows()


if __name__ == "__main__":
    init_data_set()
    """image = cv2.imread(IMAGE_DIR + '13-13.png')
    cv2.imshow('image', image)
    cv2.waitKey(0)
    colour = avg_colour(image)
    print(colour)
    for row in image:
        for pixel in row:
            pixel[0], pixel[1], pixel[2] = colour[0], colour[1], colour[2]
    cv2.imshow('image', image)
    cv2.waitKey(0)"""
    # read_images()
    print("Done")
