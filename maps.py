import png
import math
import numpy as np
import cv2
import os
from PIL import Image
import pathlib

PASSABLE = 0
IMPASSABLE = 1


def write_png_black_and_white(pixels, path):
    """
    Writes png in path according to the data in the 2d array pixels.

    pixels should be a 2d array of 1's and 0's
    0 means white
    1 means black
    """

    # if path is not string or pixels is not 2d list or tuple - exit
    if not isinstance(path, str) or not ((isinstance(pixels, list) and isinstance(pixels[0], list))
                                         or (isinstance(pixels, tuple) and isinstance(pixels[0], tuple))):
        return

    width = len(pixels[0])
    height = len(pixels)
    img = []
    for y in range(height):
        row = ()
        width = len(pixels[y])
        for x in range(width):
            color = 1 if pixels[y][x] == PASSABLE else 0
            row = row + (color,)
        img.append(row)
    with open(path, 'wb') as f:
        w = png.Writer(width, height, greyscale=True, bitdepth=1)
        w.write(f, img)


def read_png(path):
    """
    converting png img to 2d array of 0's and 1's,
    0 for pixel that was white in the original image, 1 otherwise.
    """

    r = png.Reader(path)
    width, height, rows, info = r.asRGB8()
    int_data = []
    for row in rows:
        int_values = [x for x in row]
        values = []
        for i in range(0, len(row), 3):
            values.append(PASSABLE if int_values[i] != 255 and int_values[i + 1] != 255 and int_values[i + 2] != 255
                          else IMPASSABLE)
        int_data.append(values)

    return int_data


def brush_in_pixels(pixels, x, y, diameter, color):
    """
    change values of pixels of a circle in image to a new color

    :param pixels: 2d array of pixels
    :param x: x value of the center point of circle
    :param y: y value of the center point of circle
    :param diameter: diameter length of the circle
    :param color: value the pixels in circles be changed to. 'PASSABLE' or 'IMPASSABLE'
    """
    color = PASSABLE if color == 'PASSABLE' else IMPASSABLE
    width = len(pixels[0])
    height = len(pixels)
    radius = diameter / 2
    ceil_radius = math.ceil(radius)
    x_start = x - ceil_radius if x - ceil_radius / 2 >= 0 else 0
    x_end = x + ceil_radius if x + ceil_radius <= width - 1 else width - 1
    y_start = y - ceil_radius if y - ceil_radius >= 0 else 0
    y_end = y + ceil_radius if y + ceil_radius <= height - 1 else height - 1

    for y2 in range(y_start, y_end + 1):
        for x2 in range(x_start, x_end + 1):
            dist = math.sqrt((x2 - x) ** 2 + (y2 - y) ** 2)
            if dist <= radius:
                pixels[y2][x2] = color


def generate_track(path_to_new_image, path_to_new_image_small):

    exit_code = os.system(str(pathlib.Path(__file__).parent.absolute()) + "/generator/generate.py --boundary 100 100 --span 99  -b 1 -q")

    if exit_code == 0:
        files = os.listdir("tracks")
        print(files)
        data = np.load('tracks/' + files[0])
        max_x = 0
        max_y = 0
        points = []
        for point in data:
            new_point = [int(point[0]), int(point[1])]
            points.append(new_point)
            if new_point[0] > max_x:
                max_x = new_point[0]
            if new_point[1] > max_y:
                max_y = new_point[1]

        img = [[PASSABLE for _ in range(100)] for _ in range(100)]
        for point in points:
            brush_in_pixels(img, point[0], point[1], 5, IMPASSABLE)

        write_png_black_and_white(img, path_to_new_image_small)

        src = cv2.imread(path_to_new_image_small)

        # percent by which the image is resized
        scale_percent = 900

        # calculate the 50 percent of original dimensions
        width = int(src.shape[1] * scale_percent / 100)
        height = int(src.shape[0] * scale_percent / 100)

        # d_size
        d_size = (width, height)

        # resize image
        output = cv2.resize(src, d_size)

        cv2.imwrite(path_to_new_image, output)


def convert_pixels_to_invisible(original_image_path, new_image_path):
    img = Image.open(original_image_path)
    img = img.convert("RGBA")
    data = img.getdata()

    new_data = []
    for item in data:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(new_image_path, "PNG")


generate_track('maps/map2.png', 'maps/map2_small.png')
convert_pixels_to_invisible('maps/map3.png', 'maps/map5.png')
