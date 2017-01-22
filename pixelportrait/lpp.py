from collections import defaultdict, namedtuple
from functools import partial
from itertools import izip_longest, chain
from math import sin, cos, radians
from random import sample
from time import strftime
from types import NoneType


from pixelportrait.colors import Color


class Vec(namedtuple('Vec', 'x z')):
    __slots__ = ()

    def __add__(self, other):
        return Vec(self.x + other.x, self.z + other.z)

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.z)

    def __mul__(self, other):
        return Vec(self.x * other.x, self.z * other.z)


class propertycache(object):
    def __init__(self, func):
        self._func = func
        self.__name__ = func.__name__
        self.__module__ = func.__module__
        self.__doc__ = func.__doc__

    def __get__(self, instance, owner):
        result = self._func(instance)
        setattr(instance, self.__name__, result)
        return result


def mulm(m, v):
    """Applies the specified 3x3 matrix to the given 2d (x, z) vector."""
    return Vec(
        m[0][0] * v.x + m[0][1] * 0 + m[0][2] * v[1],
        m[2][0] * v.x + m[2][1] * 0 + m[2][2] * v[1]
    )


def rotm(angle):
    """Returns a rotation matrix for the given angle in degrees around the
    vertical y-axis.
    """
    assert angle % 90 == 0
    return (lambda rad: (
        (int(cos(rad)), 0, int(sin(rad))),
        (0, 1, 0),
        (-int(sin(rad)), 0, int(cos(rad))),
    ))(radians(angle))


def rotv(angle, v):
    """Rotates the given vector by the specified angle in degrees in clockwise
    direction.
    """
    return mulm(rotm(angle), v)


def stepper(iterable, n):
    return (filter(None, c) for c in izip_longest(*([iter(iterable)] * n)))


class Brick(object):
    def __init__(self, name, nr, points, color=None, loc=Vec(0, 0), angle=0,
                 ldraw_file=None):
        assert isinstance(color, (Color, NoneType))
        self.name = name
        self.nr = nr
        self.color = color
        self._points = set(points)
        self._loc = loc
        self._angle = angle % 360
        self.ldraw_file = ldraw_file

    def rotate(self, angle):
        """Rotates the brick by the specified angle in degrees and returns a
        new Brick instance that reflects the transformation.
        """
        if angle % 90:
            raise ValueError('Only right angles are supported: %d' % angle)
        return Brick(self.name, self.nr, self._points, self.color, self._loc,
                     self._angle + angle, self.ldraw_file)

    def translate(self, vector):
        """Translates the brick along the specified vector and returns a new
        instance Brick instance that reflects the transformation.
        """
        return Brick(self.name, self.nr, self._points, self.color,
                     self._loc + vector, self._angle, self.ldraw_file)

    def paint(self, color):
        """Paints the brick and returns a new instance that reflects the new
        color.
        """
        return Brick(self.name, self.nr, self._points, color,
                     self._loc, self._angle, self.ldraw_file)

    @propertycache
    def studs(self):
        """Returns the brick's studs in LDraw coordinates."""
        return {(v + self._loc) for v in
                map(partial(rotv, self._angle), self._points)}

    def __unicode__(self):
        return 'Brick(%s, %s, %s)' % (self.name, self.nr, self.color)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def ldraw(self):
        """Returns a string describing the brick in LDraw format."""
        if not self.ldraw_file:
            raise ValueError('Brick not mapped to an ldraw object file.')
        rm = rotm(self._angle)
        return '1 %s  %s  %s %s %s  %s\r\n' % (
            self.color.code if self.color else 1,
            ' 8 '.join(map(str, self._loc)),
            ' '.join(map(str, rm[0])),
            ' '.join(map(str, rm[1])),
            ' '.join(map(str, rm[2])),
            self.ldraw_file)


class Mosaic(object):
    def __init__(self, img, bricks):
        self.img = img
        self.bricks = bricks

    def __iter__(self):
        return iter(self.bricks)

    def __len__(self):
        return len(self.bricks)

    def ldraw(self):
        """Returns a generator containing the mosaic in LDraw format."""
        yield '0 // Lego Pixel Portrait Generator\r\n'
        yield strftime('0 // Generated %H:%M:%S %d %b %Y\r\n')
        yield '0 // Erik van Zijst, erik.van.zijst@gmail.com\r\n\r\n'

        seen = set()
        for step in stepper(sorted(chain(
                *[[(s.x + s.z * self.img.width, b) for s in b.studs] for b in
                  self.bricks]), reverse=True), self.img.width):
            for _, brick in step:
                if brick not in seen:
                    yield brick.ldraw()
                    seen.add(brick)
            yield '0 STEP\r\n'


class Pixelator(object):
    def __init__(self, bricks, palette):
        self.palette = palette
        self.bricks = [
            [self._to_origin(b.rotate(a)) for a in xrange(0, 360, 90)]
            for b in bricks]

    def _to_origin(self, brick):
        """Translates a Brick instance to the origin and returns a new Brick
        instance that reflects the transformation.
        """
        return brick.translate(reduce(lambda p1, p2:
                                      Vec(max(p1.x, -p2.x), max(p1.z, -p2.z)),
                                      brick.studs, Vec(0, 0)))

    def pixelate(self, img):
        """Computes a Lego mosaic for the specified image.

        Returns a dict of colors from the palette mapped to values of sets of
        shapes.
        """
        img = img.convert('RGB').convert('L')
        try:
            colmap = {col: self.palette[i] for i, col in
                      enumerate(sorted(c[1] for c in img.getcolors()))}
        except IndexError:
            raise ValueError(
                'Image color count (%d) does not match palette width (%d)' %
                (len(img.getcolors()), len(self.palette)))

        layers = defaultdict(set)
        for i, c in enumerate(img.getdata(0)):
            layers[colmap[c]].add(Vec(i % img.width * 20, i / img.width * -20))

        bricks = set()
        for col, todo in layers.iteritems():
            for shapes in self.bricks:
                for vec in sample(list(todo), len(todo)):
                    for shape in (s.translate(vec) for s in
                                  sample(shapes, len(shapes))):
                        if all(p in todo for p in shape.studs):
                            todo.difference_update(shape.studs)
                            bricks.add(shape.paint(col))
                            break
        return Mosaic(img, bricks)
