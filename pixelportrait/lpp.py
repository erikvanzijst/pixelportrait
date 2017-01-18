from collections import defaultdict, namedtuple
from functools import partial
from itertools import chain
from operator import xor
from random import sample

Vec = namedtuple('Vector', 'x, y')


def rot(point):
    # 90 degrees clockwise rotation
    return Vec((0 - -point.y), (point.x * -1))


def trans(vector, point):
    return Vec(point.x + vector.x, point.y + vector.y)


class Shape(object):
    def __init__(self, points, bricks=()):
        self.points = set(points)
        self.bricks = set(bricks)

    def __eq__(self, other):
        return self.bricks == other.bricks and self.points == other.points

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return reduce(xor, map(hash, chain(self.bricks, self.points)), 0)

    def __unicode__(self):
        return 'Shape(%s: %s)' % (self.bricks, repr(self.points))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def trans(self, vector):
        return Shape(map(partial(trans, vector), self.points),
                     bricks=self.bricks)


class Brick(object):
    def __init__(self, name, nr, points):
        self.name = name
        self.nr = nr
        self.points = set(points)

        s = Shape(self.points, bricks={self})
        self.shapes = {s}
        for i in range(3):
            s = Brick._home(Brick._rotateshape(s))
            self.shapes.add(s)

    @staticmethod
    def _home(shape):
        return shape.trans(reduce(lambda p1, p2:
                                  Vec(max(p1.x, -p2.x), max(p1.y, -p2.y)),
                                  shape.points, Vec(0, 0)))

    @staticmethod
    def _rotateshape(shape):
        return Shape(map(rot, shape.points), bricks=shape.bricks)

    def __eq__(self, other):
        return (self.name == other.name and self.nr == other.nr and
                self.points == other.points)

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return reduce(xor, map(hash, chain(self.points, [self.name, self.nr])),
                      0)

    def __unicode__(self):
        return 'Brick(%s, %s)' % (self.name, self.nr)

    def __str__(self):
        return unicode(self).encode('utf-8')


class Mosaic(object):
    def __init__(self, shapes):
        self.shapes = shapes

    def export_ldraw(self, f):
        """Writes the mosaic as an LDraw file to the specified file object."""


class Pixelator(object):
    def __init__(self, bricks, palette):
        self.bricks = bricks
        self.palette = palette

    def pixelate(self, img):
        """Computes a Lego mosaic for the specified image.

        Returns a dict of colors from the palette mapped to values of sets of
        shapes.
        """
        img = img.convert('RGB').convert('L')
        try:
            colormap = {col: self.palette[i] for i, col in
                        enumerate(sorted(c[1] for c in img.getcolors()))}
        except IndexError:
            raise ValueError(
                'Image color count (%d) does not match palette width (%d)' %
                (len(img.getcolors()), len(self.palette)))

        layers = defaultdict(set)
        for i, c in enumerate(img.getdata(0)):
            layers[colormap[c]].add(Vec(i % img.width, i / img.width))

        shapes = defaultdict(list)
        for col, todo in layers.iteritems():
            for brick in self.bricks:
                for vec in sample(list(todo), len(todo)):
                    for shape in (s.trans(vec) for s in brick.shapes):
                        if all(p in todo for p in shape.points):
                            todo.difference_update(shape.points)
                            shapes[col].append(shape)
                            break
        return Mosaic(shapes)
