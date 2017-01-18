import pkg_resources
from unittest import TestCase

from PIL import Image

from pixelportrait.colors import BLACK, WHITE
from pixelportrait.lpp import Pixelator, Brick, Vec, Shape

PLATE1X1 = Brick('plate 1x1', 0, (Vec(0, 0),))
PLATE1X2 = Brick('plate 2x1', 3023, (Vec(0, 0), Vec(1, 0)))
PLATE2X2 = Brick('plate 2x2', 0, (Vec(0, 0), Vec(1, 0), Vec(0, 1), Vec(1, 1)))


class PixelatorTest(TestCase):

    def setUp(self):
        self.img2x2mono = Image.open(pkg_resources.resource_stream(
            PixelatorTest.__module__, 'resources/2x2_unicolor.png'))
        self.img2x2duo = Image.open(pkg_resources.resource_stream(
            PixelatorTest.__module__, 'resources/2x2_duocolor.png'))

    def test_single_layer_single_brick(self):
        pixelator = Pixelator([PLATE2X2], [BLACK])
        shapes = pixelator.pixelate(self.img2x2mono)

        self.assertItemsEqual([BLACK], shapes)
        self.assertEqual(1, len(shapes[BLACK]))
        self.assertItemsEqual(PLATE2X2.shapes, shapes[BLACK])

    def test_duo_layer_two_bricks(self):
        pixelator = Pixelator([PLATE2X2, PLATE1X2], [BLACK, WHITE])
        shapes = pixelator.pixelate(self.img2x2duo).shapes

        self.assertItemsEqual([BLACK, WHITE], shapes)
        self.assertEqual(1, len(shapes[BLACK]))
        self.assertEqual(1, len(shapes[WHITE]))
        self.assertItemsEqual(
            {Shape((Vec(0, 0), Vec(0, 1)), bricks=[PLATE1X2])},
            shapes[WHITE])
        self.assertItemsEqual(
            {Shape((Vec(1, 0), Vec(1, 1)), bricks=[PLATE1X2])},
            shapes[BLACK])

    def test_palette_mismatch(self):
        self.assertRaises(ValueError,
                          Pixelator([PLATE2X2], [BLACK, WHITE]).pixelate,
                          self.img2x2mono)
        self.assertRaises(ValueError,
                          Pixelator([PLATE2X2], [BLACK]).pixelate,
                          self.img2x2duo)
