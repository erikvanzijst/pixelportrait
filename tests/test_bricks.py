from unittest import TestCase

from pixelportrait.colors import BLACK, RED, YELLOW, BLUE
from pixelportrait.lpp import rotv, Vec,  Brick


class BrickTest(TestCase):

    def test_rotation(self):
        self.assertEqual(Vec(0, 0, 0), rotv(90, Vec(0, 0, 0)))
        self.assertEqual(Vec(-1, 0, -1), rotv(90, Vec(1, 0, -1)))
        self.assertEqual(Vec(2, 0, -2), rotv(90, Vec(2, 0, 2)))
        self.assertEqual(Vec(-2, 0, -2), rotv(180, Vec(2, 0, 2)))

    def test_translation(self):
        brick1 = Brick('1x1', 0, [Vec(0, 0, 0)])
        self.assertItemsEqual([Vec(2, -1, 2)], brick1.translate(Vec(2, -1, 2)).studs)

        brick2 = Brick('1x2', 0, [Vec(-10, 0, 0), Vec(10, 0, 0)])
        self.assertItemsEqual([Vec(-7, 0, 5), Vec(13, 0, 5)],
                              brick2.translate(Vec(3, 0, 5)).studs)

    def test_brick_rotation(self):
        brick1 = Brick('1x1x2', 0, [Vec(0, 0, 0), Vec(0, 0, 20), Vec(20, 0, 0)])
        self.assertItemsEqual([Vec(0, 0, 0), Vec(0, 0, -20), Vec(20, 0, 0)],
                              brick1.rotate(90).studs)
        self.assertItemsEqual([Vec(0, 0, 0), Vec(0, 0, 20), Vec(20, 0, 0)],
                              brick1.rotate(90).rotate(-90).studs)
        self.assertItemsEqual([Vec(0, 0, 0), Vec(0, 0, -20), Vec(-20, 0, 0)],
                              brick1.rotate(90).rotate(90).studs)
        self.assertRaises(ValueError, brick1.rotate, 1)

    def test_brick_transforms(self):
        brick = Brick('1x1x2', 0, [Vec(0, 0, 0), Vec(0, 0, 20), Vec(20, 0, 0)])
        self.assertItemsEqual(brick.translate(Vec(10, 0, 20)).rotate(180).studs,
                         brick.rotate(-90).rotate(270).translate(Vec(10, 0, 20)).studs)

    def test_brick_ldraw(self):
        self.assertRaises(ValueError, Brick('1x1', 0, [Vec(0, 0, 0)]).ldraw)
        b = Brick('1x1x2', 2420, [Vec(0, 0, 0), Vec(0, 0, 20), Vec(20, 0, 0)],
                  color=BLACK, ldraw_file='2420.dat').translate(Vec(20, 0, -40))
        print b.ldraw()
        b = b.translate(Vec(60, 0, 0)).rotate(90).paint(RED)
        print b.ldraw()
        b = b.translate(Vec(60, 0, 0)).rotate(90).paint(YELLOW)
        print b.ldraw()
        b = b.translate(Vec(60, 0, 0)).rotate(90).paint(BLUE)
        print b.ldraw()
