import png


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
            color = 0 if pixels[y][x] == 1 else 255
            row = row + (color, color, color)
        img.append(row)
    with open(path, 'wb') as f:
        w = png.Writer(width, height, greyscale=True)
        w.write(f, img)


def raw_data_to_int(rows):
    """
    Returns a 2d array of converted raw data of pixels to 0's and 1's,
    0 for pixel that was white in the original image, 1 otherwise.

    Each row in rows should be rgb values of all the pixels in the corresponding line
    of the original image (i.e. row with 2 pixels should be represented with 6 items in raw data)
    """
    int_data = []
    for row in rows:
        int_values = [x for x in row]
        values = []
        for i in range(0, len(row), 3):
            values.append(1 if int_values[i] != 255 and int_values[i + 1] != 255 and int_values[i + 2] != 255
                          else 0)
        int_data.append(values)

    return int_data


def read_png(path):
    """
    converting png img to 2d array of 0's and 1's,
    0 for pixel that was white in the original image, 1 otherwise.
    """

    r = png.Reader(path)
    _, _, rows, _ = r.read()

    return raw_data_to_int(rows)



