#!/usr/bin/env python
import argparse
import sys

from PIL import Image

from pixelportrait.bricks import (PLATE1X2, PLATE2X2, CORNER2X2, PLATE1X1,
                                  PLATE1X3)
from pixelportrait.colors import BLUES, YELLOWS
from pixelportrait.lpp import Pixelator


BRICKS = (PLATE2X2, CORNER2X2, PLATE1X3, PLATE1X2, PLATE1X1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Turns an image into a Lego pixel-portrait. The image '
                    'must use 5 colors only.')
    parser.add_argument('-p', '--palette', choices=('blue', 'orange', 'gray'),
                        default='orange', dest='pal',
                        help='the Lego color palette to use')
    parser.add_argument('-o', '--out', dest='file',
                        help='write to file (stdout when omitted)')
    parser.add_argument('image', nargs='?',
                        help='the image file (stdin if omitted)')
    args = parser.parse_args()

    map((open(args.file, 'w') if args.file else sys.stdout).write,
        Pixelator(BRICKS, {'blue': BLUES, 'orange': YELLOWS}[args.pal])
        .pixelate(Image.open(sys.stdin if (args.image in ('-', None)) else args.image)).ldraw())
