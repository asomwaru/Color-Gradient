import argparse
import gradient as grad
from random import randint

# from pprint import pprint

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--start', dest='start_color', type=int, action='store', nargs=3, default=None,
                    help="Starting color. If none then a random starting value will be used.")

parser.add_argument('-d', '--dir', '--direction', dest='directions', type=str, action='store', default='XNN',
                    help="Directions for rgb to go in.")

parser.add_argument('-g', '--grid', dest='grid', action='store_true', help="Save as color grid.")

parser.add_argument('-l', '--length', dest='length', type=int, action='store', default=900, help="Length of image.")

parser.add_argument('-w', '--width', dest='width', type=int, action='store', default=900, help="Width of image.")

parser.add_argument('-b', '--brightness', dest='brightness', type=int, action='store', nargs=3, default=None,
                    help="Bright for each rgb value. if none then a random value will be used.")

parser.add_argument('-m', '--mini', dest='mini', action='store_true', help="Save as a mini color grid.")

args = parser.parse_args()

if args.start_color is None:
    args.start_color = tuple([randint(0, 255) for _ in range(3)])
else:
    args.start_color = tuple(args.start_color)

suggested_val = grad.common_factor(args.length, args.width)

if args.length <= 1000 or args.width <= 1000:
    bright = [0] * 3
    for i, x in enumerate(args.directions):
        if x == 'Y':
            bright[i] = randint(4, 8)
        elif x == 'X':
            bright[i] = randint(4, 8)
        else:
            continue

    args.brightness = tuple(bright)

elif args.brightness is None:
    bright = [0] * 3
    for i, x in enumerate(args.directions):
        if x == 'Y':
            bright[i] = args.length // suggested_val
        elif x == 'X':
            bright[i] = args.width // suggested_val
        else:
            continue

    args.brightness = tuple(bright)

else:
    args.brightness = tuple(args.brightness)

args = vars(args)

if args['mini']:
    if args['length'] <= 1000 or args['width'] <= 1000:
        gradient_pic = grad.convert_to_image(**args, save=False)
        new_pic = grad.average_chunks(gradient_pic, 100, 100, save=True)
    else:
        gradient_pic = grad.convert_to_image(**args, save=False)
        new_pic = grad.average_chunks(gradient_pic, suggested_val, suggested_val, save=True)

elif args['grid']:
    if args['length'] <= 1000 or args['width'] <= 1000:
        gradient_pic = grad.convert_to_image(**args, save=False)
        new_pic = grad.average_chunks(gradient_pic, 100, 100)
        grad.upscale(new_pic, 100, True)
    else:
        gradient_pic = grad.convert_to_image(**args, save=False)
        new_pic = grad.average_chunks(gradient_pic, suggested_val, suggested_val)
        grad.upscale(new_pic, suggested_val, True)

else:
    gradient_pic = grad.convert_to_image(**args)
