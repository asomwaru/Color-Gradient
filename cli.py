import argparse
import gradient as grad

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--start', dest='start_color', type=int, action='store', nargs=3, default=(255, 0, 128),
                    help="Starting color.")

parser.add_argument('-d', '--dir', '--direction', dest='directions', type=str, action='store', default='XNN',
                    help="Directions for rgb to go in.")

parser.add_argument('-g', '--grid', dest='grid', action='store_true', help="Save as color grid.")

parser.add_argument('-l', '--length', dest='length', type=int, action='store', default=900, help="Length of image.")

parser.add_argument('-w', '--width', dest='width', type=int, action='store', default=900, help="Width of image.")

parser.add_argument('-b', '--brightness', dest='brightness', type=int, action='store', nargs=3, default=(4, 0, 0),
                    help="Bright for each rgb value.")

parser.add_argument('-m', '--mini', dest='mini', action='store_true', help="Save as a mini color grid.")

args = parser.parse_args()

args.brightness = tuple(args.brightness)
args.start_color = tuple(args.start_color)
suggested_val = max(grad.common_factor(args['length'], args['width']))

if args.mini:
    args = vars(args)

    gradient_pic = grad.convert_to_image(**args, save=False)
    new_pic = grad.average_chunks(gradient_pic, suggested_val, suggested_val, save=True)

elif args.grid:
    args = vars(args)

    rows = args['rows']
    cols = args['columns']

    gradient_pic = grad.convert_to_image(**args, save=False)
    new_pic = grad.average_chunks(gradient_pic, suggested_val, suggested_val)
    grad.upscale(new_pic, suggested_val, True)

else:
    args = vars(args)
    gradient_pic = grad.convert_to_image(**args)
