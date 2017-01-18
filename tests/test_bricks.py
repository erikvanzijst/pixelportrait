from unittest import TestCase

from pixelportrait.lpp import rot, Vec, trans, Shape, Brick


class BrickTest(TestCase):

    def test_rotation(self):
        self.assertEqual(Vec(0, 0), rot(Vec(0, 0)))
        self.assertEqual(Vec(-1, -1), rot(Vec(1, -1)))
        self.assertEqual(Vec(2, -2), rot(Vec(2, 2)))

    def test_translation(self):
        self.assertEqual(Vec(2, 2), trans(Vec(2, 2), Vec(0, 0)))
        self.assertEqual(Vec(1, 3), trans(Vec(3, 5), Vec(-2, -2)))
        self.assertSetEqual(
            {Vec(3, -5), Vec(3, -4)},
            set(Shape((Vec(0, 0), Vec(0, 1))).trans(Vec(3, -5)).points))

    def test_brick_equality(self):
        self.assertEqual(Brick('test', 0, []), Brick('test', 0, []))
        self.assertEqual(Brick('test', 0, [Vec(0, 0)]),
                         Brick('test', 0, [Vec(0, 0)]))
        self.assertEqual(Brick('test', 0, [Vec(0, 0), Vec(1, 0)]),
                         Brick('test', 0, [Vec(1, 0), Vec(0, 0)]))

        self.assertNotEqual(Brick('test', 0, [Vec(0, 0), Vec(1, 1)]),
                            Brick('test', 0, [Vec(0, 0), Vec(0, 1)]))

    def test_shape_equality(self):
        brick1 = Brick('1x1', 0, [Vec(0, 0)])

        self.assertEqual(Shape([]), Shape([]))
        self.assertEqual(Shape([Vec(0, 0), Vec(5, 5)]),
                         Shape([Vec(0, 0), Vec(5, 5)]))
        self.assertEqual(Shape([Vec(0, 0), Vec(5, 5)], [brick1]),
                         Shape([Vec(0, 0), Vec(5, 5)], [brick1]))

        self.assertNotEqual(Shape([]), Shape([], [brick1]))
        self.assertNotEqual(Shape([Vec(0, 0), Vec(5, 6)]),
                            Shape([Vec(0, 0), Vec(5, 5)]))

    def test_brick_shapes(self):
        brick1 = Brick('1x1', 0, [Vec(0, 0)])
        self.assertSetEqual({Shape((Vec(0, 0),), bricks=[brick1])},
                            brick1.shapes)

        brick2 = Brick('2x1', 1, [Vec(0, 0), Vec(1, 0), Vec(2, 0)])
        self.assertSetEqual(
            {Shape((Vec(0, 0), Vec(1, 0), Vec(2, 0)), bricks=[brick2]),
             Shape((Vec(0, 0), Vec(0, 1), Vec(0, 2)), bricks=[brick2])},
            brick2.shapes)

        brick3 = Brick('2x2', 1, [Vec(0, 0), Vec(1, 0), Vec(0, 1), Vec(1, 1)])
        self.assertSetEqual({Shape((Vec(0, 0), Vec(1, 0), Vec(0, 1), Vec(1, 1)),
                                   bricks=[brick3])},
                            brick3.shapes)

        brick4 = Brick('2x2 corner tile', 1, [Vec(0, 0), Vec(1, 0), Vec(0, 1)])
        self.assertSetEqual(
            {Shape((Vec(0, 0), Vec(1, 0), Vec(0, 1)), bricks=[brick4]),
             Shape((Vec(0, 0), Vec(1, 1), Vec(0, 1)), bricks=[brick4]),
             Shape((Vec(1, 1), Vec(1, 0), Vec(0, 1)), bricks=[brick4]),
             Shape((Vec(0, 0), Vec(1, 0), Vec(1, 1)), bricks=[brick4])
             }, brick4.shapes)
