#!/usr/bin/env python
import argparse
import sys
from io import BytesIO
from itertools import chain
from tempfile import NamedTemporaryFile
from time import strftime

from PIL import Image
from subprocess import Popen, PIPE

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
GRAYS = (col.BLACK, col.DARK_BLUISH_GRAY, col.LIGHT_BLUISH_GRAY, col.WHITE)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Turns an image into a Lego pixel-portrait.')
    parser.add_argument('-p', '--palette', choices=('blue', 'orange', 'gray'),
                        default='orange', dest='pal',
                        help='the Lego color palette to use')
    parser.add_argument('-n', '--no-studs', dest='tiles', action='store_true',
                        help='use tiles without studs')
    parser.add_argument('-d', '--dimensions', dest='dim', default='48x48',
                        type=lambda v: tuple(int(i) for i in v.split('x', 1)),
                        help='width and height in studs (48x48 when omitted)')
    parser.add_argument('-o', '--out', dest='file',
                        help='write to file (stdout when omitted)')
    parser.add_argument('image', nargs='?',
                        help='the image file (stdin when omitted)')
    args = parser.parse_args()

    img = Image.open(BytesIO(sys.stdin.read()) if (args.image in ('-', None))
                     else args.image)
    palette = {'blue': BLUES, 'orange': YELLOWS, 'gray': GRAYS}[args.pal]

    # pre-processing: crop to desired aspect ratio and reduce color count:
    if img.width / float(args.dim[0]) < img.height / float(args.dim[1]):
        w = img.width
        h = int(args.dim[1] * (img.width / float(args.dim[0])))
    else:
        w = int(args.dim[0] * (img.height / float(args.dim[1])))
        h = img.height

    p = Popen(
        'convert - -resize {w}x{h}^ -gravity center -extent {w}x{h} png:- | '
        'convert - +dither -colors {colors} -'.format(
            w=w, h=h, colors=len(palette)),
        shell=True, stdin=PIPE, stdout=PIPE)
    img.save(p.stdin, format='png')
    p.stdin.close()
    img = p.stdout.read()
    assert not p.wait()

    with NamedTemporaryFile() as colors:
        # extract quantized gray scale color map
        p = Popen('convert - -colorspace Gray -unique-colors %s' %
                  colors.name, shell=True, stdin=PIPE)
        p.stdin.write(img)
        p.stdin.close()
        assert not p.wait()

        # resize with custom color map
        p = Popen('convert - -colorspace Gray - | '
                  'convert - -resize {w}x{h}^ -gravity center -extent {w}x{h}'
                  ' -remap {colors} +dither -'.format(w=args.dim[0], h=args.dim[1], colors=colors.name),
                  shell=True, stdin=PIPE, stdout=PIPE)
        p.stdin.write(img)
        p.stdin.close()
        img = Image.open(BytesIO(p.stdout.read()))
        assert not p.wait()

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
        ), Pixelator(TILES if args.tiles else PLATES, palette)
            .pixelate(img).ldraw()))
