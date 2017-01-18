from collections import namedtuple

from ansicolor import rgb2short


class Color(namedtuple('Color_', 'blname blcode html')):
    # http://ryanhowerter.net/colors.html
    # https://www.bricklink.com/catalogColors.asp
    __slots__ = ()
    @property
    def rgb(self):
        return (lambda c:
                (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)))(self.html)

    @property
    def ansi(self):
        return rgb2short(self.html)[0]


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
