import numpy as np
from PIL import Image, ImageDraw


def convert_to_image(width: int = 900, length: int = 900, start_color: tuple = (0, 255, 128), brightness: int = 4,
                     save: bool = True):
    """
    Args:
        width: Width of image. Defaults to 900
        length: Length of image. Defaults to 900
        start_color: Starting rgb value for gradient
        brightness: Brightness for gradient progression. Values must be 4 or more for gradient to be correct

    Returns:
        arr: The array of color values for the picture

    Raises:
        ValueError: If dimensions are less than 0 or if brightness is less than 4
    """
    if length <= 0 or width <= 0:
        raise ValueError("Dimensions cannot be less than 0.")

    if brightness < 4:
        raise ValueError("Brightness cannot be less 4 for gradient.")

    l, w = length, width
    arr = np.array(Image.new('RGB', (w, l), color=start_color))

    for y in range(l):
        for x in range(w):
            arr[y, x][0] = (y / brightness)
            arr[y, x][1] = (x / 6)
            # arr[y, x][2] = (x / 6)
            pass

    if save:
        Image.fromarray(arr.astype('uint8'), 'RGB').save("gradient.png")

    return arr


def average_chunks(picture: np.array, rows: int, cols: int, save: bool = False):
    """
    Args:
         picture: Array of rgb values for picture gradient
         rows: How many rows for descaled picture
         cols: How many columns for descaled picture
         save: To save picture or not

    Return:
        new_pic: Averaged picture array

    Raises:
        ValueError: If rows or cols do not divide easily into passed picture
    """
    pic_y, pic_x, _ = picture.shape
    if pic_y % rows != 0:
        raise ValueError("Rows do not split the image perfectly.")

    if pic_x % cols != 0:
        raise ValueError("Columns do not split the image perfectly.")

    new_pic = np.array(Image.new('RGB', (pic_x // cols, pic_y // rows), color=(255, 255, 255)))

    for y in range(pic_y // rows):
        for x in range(pic_x // cols):
            mat = picture[y * rows:(y * rows) + rows, x * cols:(x * cols) + cols]

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


def upscale(picture: np.array, size: int):
    """
    Args:
         picture: Picture array
         size: rgb upscale value

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

    im.save('new_pic.png')


if __name__ == '__main__':
    grad = convert_to_image()
    new = average_chunks(grad, 100, 100)
    upscale(new, 100)
