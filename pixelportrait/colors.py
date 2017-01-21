from collections import namedtuple


class Color(namedtuple('Color_', 'name code html')):
    # We're using BrickLink names and codes.
    # http://ryanhowerter.net/colors.html
    # https://www.bricklink.com/catalogColors.asp
    __slots__ = ()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return unicode(self).encode('utf-8')


BLACK = Color('black', 11, '1b2a34')
WHITE = Color('white', 1, 'f4f4f4')

RED = Color('red', 5, 'b40000')
ORANGE = Color('orange', 4, 'd67923')
YELLOW = Color('yellow', 3, 'fac80a')

DARK_BLUE = Color('dark blue', 63, '19325a')
BLUE = Color('blue', 7, '1e5aa8')
MEDIUM_BLUE = Color('medium blue', 42, '7396c8')


BLUES = (BLACK, DARK_BLUE, BLUE, MEDIUM_BLUE, WHITE)
YELLOWS = (BLACK, RED, ORANGE, YELLOW, WHITE)
