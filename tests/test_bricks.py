from unittest import TestCase

from pixelportrait.colors import BLACK, RED, YELLOW, BLUE
from pixelportrait.lpp import rotv, Vec,  Brick


class BrickTest(TestCase):

    def test_rotation(self):
        self.assertEqual(Vec(0, 0), rotv(90, Vec(0, 0)))
        self.assertEqual(Vec(-1, -1), rotv(90, Vec(1, -1)))
        self.assertEqual(Vec(2, -2), rotv(90, Vec(2, 2)))
        self.assertEqual(Vec(-2, -2), rotv(180, Vec(2, 2)))

    def test_translation(self):
        brick1 = Brick('1x1', 0, [Vec(0, 0)])
        self.assertItemsEqual([Vec(2, 2)], brick1.translate(Vec(2, 2)).studs)

        brick2 = Brick('1x2', 0, [Vec(-10, 0), Vec(10, 0)])
        self.assertItemsEqual([Vec(-7, 5), Vec(13, 5)],
                              brick2.translate(Vec(3, 5)).studs)

    def test_brick_equality(self):
        self.assertEqual(Brick('test', 0, []), Brick('test', 0, []))
        self.assertEqual(Brick('test', 0, [Vec(0, 0)]),
                         Brick('test', 0, [Vec(0, 0)]))
        self.assertEqual(Brick('test', 0, [Vec(0, 0), Vec(1, 0)], angle=360),
                         Brick('test', 0, [Vec(1, 0), Vec(0, 0)]))
        self.assertEqual(Brick('test', 0, [Vec(0, 0), Vec(1, 0)], angle=-90),
                         Brick('test', 0, [Vec(1, 0), Vec(0, 0)], angle=270))

        self.assertNotEqual(Brick('test', 0, [Vec(0, 0), Vec(1, 1)]),
                            Brick('test', 0, [Vec(0, 0), Vec(0, 1)]))
        self.assertNotEqual(Brick('test', 0, [Vec(0, 0), Vec(1, 1)], angle=90),
                            Brick('test', 0, [Vec(0, 0), Vec(1, 1)]))

    def test_brick_rotation(self):
        brick1 = Brick('1x1x2', 0, [Vec(0, 0), Vec(0, 20), Vec(20, 0)])
        self.assertItemsEqual([Vec(0, 0), Vec(0, -20), Vec(20, 0)],
                              brick1.rotate(90).studs)
        self.assertItemsEqual([Vec(0, 0), Vec(0, 20), Vec(20, 0)],
                              brick1.rotate(90).rotate(-90).studs)
        self.assertItemsEqual([Vec(0, 0), Vec(0, -20), Vec(-20, 0)],
                              brick1.rotate(90).rotate(90).studs)
        self.assertRaises(ValueError, brick1.rotate, 1)

    def test_brick_transforms(self):
        brick = Brick('1x1x2', 0, [Vec(0, 0), Vec(0, 20), Vec(20, 0)])
        self.assertEqual(brick.translate(Vec(10, 20)).rotate(180),
                         brick.rotate(-90).rotate(270).translate(Vec(10, 20)))

    def test_brick_ldraw(self):
        self.assertRaises(ValueError, Brick('1x1', 0, [Vec(0, 0)]).ldraw)
        b = Brick('1x1x2', 2420, [Vec(0, 0), Vec(0, 20), Vec(20, 0)],
                  color=BLACK, ldraw_file='2420.dat').translate(Vec(20, -40))
        print b.ldraw()
        b = b.translate(Vec(60, 0)).rotate(90).paint(RED)
        print b.ldraw()
        b = b.translate(Vec(60, 0)).rotate(90).paint(YELLOW)
        print b.ldraw()
        b = b.translate(Vec(60, 0)).rotate(90).paint(BLUE)
        print b.ldraw()
