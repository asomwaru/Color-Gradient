import numpy as np
from PIL import Image, ImageDraw
from math import gcd


def convert_to_image(width: int = 900, length: int = 900, start_color: tuple = (0, 255, 128),
                     save: bool = True, directions: str = "XNN", brightness: tuple = (4, 4, 4), **kwargs):
    """
    Args:
        width: Width of image. Defaults to 900
        length: Length of image. Defaults to 900
        start_color: Starting rgb value for gradient
        brightness: Brightness for gradient progression. Values must be 4 or more for gradient to be correct
        directions: 3 letters for the rgb which are 'N', 'X', 'Y'
        brightness: brightness for each of the rgb directions

    Returns:
        arr: The array of color values for the picture

    Raises:
        ValueError: If dimensions are less than 0 or if bright variables do not meet requirement
    """
    if length <= 0 or width <= 0:
        raise ValueError("Dimensions cannot be less than 0.")

    directions = directions.upper()

    if directions is None:
        raise ValueError("Must supply directions for gradient")
    elif len(directions) != 3:
        raise ValueError("Must have 3 direction values ('N', 'X', 'Y').")
    elif sum([directions.count('X'), directions.count('Y'), directions.count('N')]) != 3:
        raise ValueError("Wrong values supplied for directions.")

    if len(brightness) != 3:
        raise ValueError("Must supply 3 values. Put 0 if rgb value is N.")

    for i, x in zip(brightness, directions):
        if x == 'N':
            continue

        if x == 'X':
            val = (width / i) / width
        else:
            val = (length / i) / length

        if val < 0.1:
            raise ValueError("Brightness scale is too low, will cause repeated values.")

    l, w = length, width
    arr = np.array(Image.new('RGB', (w, l), color=start_color))

    for y in range(l):
        for x in range(w):
            if directions[0] == 'X':
                arr[y, x][0] = x / brightness[0]
            elif directions[0] == 'Y':
                arr[y, x][0] = y / brightness[0]

            if directions[1] == 'X':
                arr[y, x][1] = x / brightness[1]
            elif directions[1] == 'Y':
                arr[y, x][1] = y / brightness[1]

            if directions[2] == 'X':
                arr[y, x][2] = x / brightness[2]
            elif directions[2] == 'Y':
                arr[y, x][2] = y / brightness[2]

    if save:
        Image.fromarray(arr.astype('uint8'), 'RGB').save("gradient.png")

    return arr


def average_chunks(picture: np.array, y_scale: int, x_scale: int, save: bool = False):
    """
    Args:
         picture: Array of rgb values for picture gradient
         y_scale: Number to descale y by
         x_scale: Number to descale x by
         save: save the picture

    Return:
        new_pic: Averaged picture array

    Raises:
        ValueError: If rows or cols do not divide easily into passed picture
    """
    pic_y, pic_x, _ = picture.shape

    if pic_y % y_scale != 0:
        raise ValueError("Rows do not split the image perfectly. Suggest value would be {}.".format(
            common_factor(pic_x, pic_y)))

    if pic_x % x_scale != 0:
        raise ValueError("Columns do not split the image perfectly. Suggest value would be {}".format(
            common_factor(pic_x, pic_y)))

    new_pic = np.array(Image.new('RGB', (pic_x // x_scale, pic_y // y_scale), color=(255, 255, 255)))

    for y in range(pic_y // y_scale):
        for x in range(pic_x // x_scale):
            mat = picture[y * y_scale:(y * y_scale) + y_scale, x * x_scale:(x * x_scale) + x_scale]

            values = np.array([j for i in mat for j in i])

            r = np.sum(values[:, 0]) // len(values[:, 0])
            g = np.sum(values[:, 1]) // len(values[:, 1])
            b = np.sum(values[:, 2]) // len(values[:, 2])

            new_pic[y, x][0] = r
            new_pic[y, x][1] = g
            new_pic[y, x][2] = b

    if save:
        Image.fromarray(new_pic.astype('uint8'), 'RGB').save('new_pic.png')

    return new_pic


def upscale(picture: np.array, size: int, save: bool = True):
    """
    Args:
         picture: Picture array
         size: rgb upscale value
         save: To save image or not

    Raises:
        ValueError: If size is less than 0
    """

    if size <= 0:
        raise ValueError("Cannot upscale image with value less than 1.")

    pic_y, pic_x, _ = picture.shape

    im = Image.new('RGB', (pic_x * size, pic_y * size), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    for y in range(pic_y):
        for x in range(pic_x):
            draw.rectangle([(x * size, y * size), ((x + 1) * size, (y + 1) * size)], fill=tuple(picture[y, x]))

    if save:
        im.save('new_pic.png')


def common_factor(num1, num2):
    n = []
    g = gcd(num1, num2)
    for i in range(1, g + 1):
        if g % i == 0:
            n.append(i)
    return max(n)

# if __name__ == '__main__':
#     grad = convert_to_image(length=1050, width=1680, directions="XYN", brightness=(8, 5, 0))
#     new = average_chunks(grad, 180, 180)
#     upscale(new, 180)
