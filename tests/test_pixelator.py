import pkg_resources
from unittest import TestCase

from PIL import Image

from pixelportrait.bricks import PLATE2X2, PLATE1X2
from pixelportrait.colors import BLACK, WHITE
from pixelportrait.lpp import Pixelator


class PixelatorTest(TestCase):

    def setUp(self):
        self.img2x2mono = Image.open(pkg_resources.resource_stream(
            PixelatorTest.__module__, 'resources/2x2_unicolor.png'))
        self.img2x2duo = Image.open(pkg_resources.resource_stream(
            PixelatorTest.__module__, 'resources/2x2_duocolor.png'))

    def test_single_layer_single_brick(self):
        pixelator = Pixelator([PLATE2X2], [BLACK])
        mosaic = pixelator.pixelate(self.img2x2mono)

        self.assertEqual(1, len(mosaic.bricks))
        self.assertEqual(BLACK, next(iter(mosaic)).color)

        lines = [l for l in mosaic.ldraw() if l.startswith('1 ')]
        self.assertEqual(1, len(lines))
        self.assertIn(' 10 0 10 ', lines[0])

    def test_duo_layer_two_bricks(self):
        pixelator = Pixelator([PLATE2X2, PLATE1X2], [BLACK, WHITE])
        mosaic = pixelator.pixelate(self.img2x2duo)

        self.assertEqual(2, len(mosaic.bricks))

    def test_palette_mismatch(self):
        self.assertRaises(ValueError, Pixelator([PLATE2X2], [BLACK]).pixelate,
                          self.img2x2duo)
