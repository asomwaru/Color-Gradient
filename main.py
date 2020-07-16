import numpy as np
from PIL import Image

START_COLOR = (255, 0, 128)
BRIGHTNESS = 4

np.arange(12)

def convert_to_image():
    l, w = 900, 900
    arr = np.array(Image.new('RGB', (w, l), color=START_COLOR))

    for y in range(l):
        for x in range(w):
            arr[y, x][0] = (y / BRIGHTNESS)
            arr[y, x][1] = (x / 6)
            # arr[y, x][2] = (x / 6)
            pass

    new_img = Image.fromarray(arr.astype('uint8'), 'RGB')
    new_img.save('gradient.png')

    return arr

if __name__ == '__main__':
    convert_to_image()