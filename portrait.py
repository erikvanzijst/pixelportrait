#!/usr/bin/env python
import argparse
import sys
from itertools import chain
from time import strftime

from PIL import Image

from pixelportrait import bricks
from pixelportrait import colors as col
from pixelportrait.lpp import Pixelator, Vec

BASES = {(32, 32): bricks.BASE32X32, (48, 48): bricks.BASE48X48,
         (50, 50): bricks.BASE50X50}
PLATES = (
    bricks.PLATE2X3,
    # bricks.PLATE1X4,
    bricks.PLATE2X2,
    # bricks.CORNER2X2,
    # bricks.PLATE1X3,
    bricks.PLATE1X2,
    bricks.PLATE1X1)
TILES = (
    bricks.TILE2X2,
    bricks.TILE1X2,
    bricks.TILE1X1
)
BLUES = (col.BLACK, col.DARK_BLUE, col.BLUE, col.MEDIUM_BLUE, col.WHITE)
YELLOWS = (col.BLACK, col.RED, col.ORANGE, col.YELLOW, col.WHITE)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Turns an image into a Lego pixel-portrait. The image '
                    'must use 5 colors only.')
    parser.add_argument('-p', '--palette', choices=('blue', 'orange'),
                        default='orange', dest='pal',
                        help='the Lego color palette to use')
    parser.add_argument('-n', '--no-studs', dest='tiles', action='store_true',
                        help='use tiles without studs')
    parser.add_argument('-o', '--out', dest='file',
                        help='write to file (stdout when omitted)')
    parser.add_argument('image', nargs='?',
                        help='the image file (stdin if omitted)')
    args = parser.parse_args()

    img = Image.open(sys.stdin if (args.image in ('-', None)) else args.image)
    base = BASES.get((img.width, img.height))

    map((open(args.file, 'w') if args.file else sys.stdout).write,
        chain((
            '0 // Lego Pixel Portrait Generator\r\n',
            strftime('0 // Generated %H:%M:%S %d %b %Y\r\n'),
            '0 // Erik van Zijst, erik.van.zijst@gmail.com\r\n\r\n',

            base.translate(reduce(lambda p1, p2:
                                  Vec(max(p1.x, -p2.x),
                                      min(p1.y, -p2.y),
                                      min(p1.z, -p2.z)),
                                  base.studs, Vec(0, 0, 0)))
                .translate(Vec(0, 8, 0)).ldraw() if base else ''
        ), Pixelator(TILES if args.tiles else PLATES,
                     {'blue': BLUES, 'orange': YELLOWS}[args.pal])
            .pixelate(img).ldraw()))
