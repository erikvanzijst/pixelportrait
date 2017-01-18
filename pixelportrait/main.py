import argparse

from PIL import Image

from pixelportrait.colors import BLUES, YELLOWS
from pixelportrait.lpp import Brick, Pixelator, Vec

BRICKS = (Brick('plate 2x2', 0, (Vec(0, 0), Vec(1, 0), Vec(0, 1), Vec(1, 1))),
          Brick('corner plate 2x2', 0, (Vec(0, 0), Vec(1, 0), Vec(0, 1))),
          Brick('plate 3x1', 0, (Vec(0, 0), Vec(1, 0), Vec(0, 1))),
          Brick('plate 2x1', 3023, (Vec(0, 0), Vec(1, 0))),
          Brick('plate 1x1', 0, (Vec(0, 0),)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Turns an image into a Lego pixel-portrait. The image '
                    'must use 5 colors only.')
    parser.add_argument('-p', '--palette', choices=('blue', 'orange', 'gray'),
                        default='orange', dest='pal',
                        help='the Lego color palette to use')
    parser.add_argument('image', help='the image file')
    args = parser.parse_args()

    shapes = (Pixelator(BRICKS, {'blue': BLUES, 'orange': YELLOWS}[args.pal])
              .pixelate(Image.open(args.image)))
