import random
import sys
from collections import defaultdict
from collections import namedtuple

from PIL import Image
from colored import fg, bg, attr


class Color(namedtuple('Color_', 'blname blcode html lgname lgcode ansi')):
    # http://ryanhowerter.net/colors.html
    # https://www.bricklink.com/catalogColors.asp
    __slots__ = ()
    @property
    def rgb(self):
        return (lambda c:
                (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)))(self.html)

BLACK = Color('black', 11, '1b2a34', 'black', 26, 0)
RED = Color('red', 5, 'b40000', 'bright red', 21, 1)
ORANGE = Color('orange', 4, 'd67923', 'bright orange', 106, 166)
BRIGHT_LIGHT_ORANGE = Color('bright light orange', 110, 'fcac00',
                            'flame yellowish orange', 191, 208)
YELLOW = Color('yellow', 3, 'fac80a', 'bright yellow', 24, 214)
WHITE = Color('white', 1, 'f4f4f4', 'white', 1, 15)

DARK_BLUE = Color('dark blue', 63, '19325a', 'earth blue', 140, 19)
BLUE = Color('blue', 7, '1e5aa8', 'bright blue', 23, 21)
MEDIUM_BLUE = Color('medium blue', 42, '7396c8', 'medium blue', 102, 74)

yellows = (BLACK, RED, ORANGE, YELLOW, BRIGHT_LIGHT_ORANGE, WHITE)
# hex codes to brick link color names
rgb_to_index = {c.rgb: i for i, c in enumerate(yellows)}

if __name__ == '__main__':
    img = Image.open(sys.argv[1]).convert('RGB')
    width, height = img.width, img.height
    pixels = [[rgb_to_index[img.getpixel((x, y))] for y in range(height)]
              for x in range(width)]
    raster = [[u'  ' for y in range(height)] for x in range(width)]

    def randcoord():
        return random.randint(0, width - 1), random.randint(0, height - 1)

    def randbrick():
        while True:
            coord = randcoord()
            if random.randint(0, 1):
                if coord[0] == width - 1:
                    continue
                return coord, (coord[0] + 1, coord[1])
            else:
                if coord[1] == height - 1:
                    continue
                return coord, (coord[0], coord[1] + 1)

    def stats():
        tiles = defaultdict(int)
        singles = defaultdict(int)
        for x in range(width):
            for y in range(height):
                color = yellows[pixels[x][y]]
                px = raster[x][y]
                if u'\u23b4' in px or u'[' in px:
                    tiles[color] += 1
                elif px == u'  ':
                    singles[color] += 1
        print '\n'.join('1x2 %s%s%s: %d' % (fg(c.ansi), c.blname, attr('reset'), n) for c, n in tiles.iteritems())
        print '\n'.join('1x1 %s%s%s: %d' % (fg(c.ansi), c.blname, attr('reset'), n) for c, n in singles.iteritems())
        print 'Total bricks: %d' % (sum(tiles.values()) + sum(singles.values()))

    for i in xrange(50000):
        color = random.randint(0, len(yellows) - 1)
        p1, p2 = randbrick()
        if pixels[p1[0]][p1[1]] == color and pixels[p2[0]][p2[1]] == color:
            if raster[p1[0]][p1[1]] == u'  ' and raster[p2[0]][p2[1]] == u'  ':
                if p1[0] == p2[0]:
                    # vertical
                    raster[p1[0]][p1[1]] = u'\u23b4 '
                    raster[p2[0]][p2[1]] = u'\u23b5 '
                else:
                    # horizontal
                    raster[p1[0]][p1[1]] = u'[ '
                    raster[p2[0]][p2[1]] = u' ]'

    print '   ' + ''.join(('%2d' % (n+1) for n in xrange(width)))
    for y in range(height):
        sys.stdout.write('%2d ' % (y + 1))
        for x in range(width):
            ansi = yellows[pixels[x][y]].ansi
            sys.stdout.write((u'%s%s' % (bg(ansi), raster[x][y])).encode('utf-8'))
        sys.stdout.write('%s\n' % attr('reset'))
    sys.stdout.write('\n')
    sys.stdout.flush()
    stats()
