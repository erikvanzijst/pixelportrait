from collections import namedtuple


class Color(namedtuple('Color_', 'name code')):
    # We're using Lego names and LDraw codes.
    # http://www.ldraw.org/article/547.html
    __slots__ = ()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return unicode(self).encode('utf-8')


BLACK = Color('black', 0)
WHITE = Color('white', 15)

RED = Color('red', 4)
ORANGE = Color('orange', 25)
YELLOW = Color('yellow', 14)

DARK_BLUE = Color('dark blue', 272)
BLUE = Color('blue', 1)
MEDIUM_BLUE = Color('medium blue', 73)


BLUES = (BLACK, DARK_BLUE, BLUE, MEDIUM_BLUE, WHITE)
YELLOWS = (BLACK, RED, ORANGE, YELLOW, WHITE)
