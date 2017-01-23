from pixelportrait.colors import GREY
from pixelportrait.lpp import Brick, Vec

BASE32X32 = Brick('plate 32x32', 3811,
                  (Vec(-310, 0, 310), Vec(310, 0, 310),
                   Vec(-310, 0, -310), Vec(310, 0, -310)), GREY,
                  ldraw_file='3811.dat')
BASE48X48 = Brick('plate 48x48', 4186,
                  (Vec(-470, 0, 470), Vec(470, 0, 470),
                   Vec(-470, 0, -470), Vec(470, 0, -470)), GREY,
                  ldraw_file='4186.dat')
BASE50X50 = Brick('plate 50x50', 782,
                  (Vec(-490, 0, 490), Vec(490, 0, 490),
                   Vec(-490, 0, -490), Vec(490, 0, -490)), GREY,
                  ldraw_file='782.dat')

PLATE1X1 = Brick('plate 1x1', 3024, (Vec(0, 0, 0),), ldraw_file='3024.dat')
TILE1X1 = Brick('tile 1x1', 3070, (Vec(0, 0, 0),), ldraw_file='3070b.dat')
PLATE1X2 = Brick('plate 2x1', 3023, (Vec(-10, 0, 0), Vec(10, 0, 0)),
                 ldraw_file='3023.dat')
TILE1X2 = Brick('tile 2x1', 3069, (Vec(-10, 0, 0), Vec(10, 0, 0)),
                ldraw_file='3069b.dat')
PLATE1X3 = Brick('plate 1x3', 3623,
                 (Vec(-20, 0, 0), Vec(0, 0, 0), Vec(20, 0, 0)),
                 ldraw_file='3623.dat')
TILE1X3 = Brick('tile 1x3', 63864,
                (Vec(-20, 0, 0), Vec(0, 0, 0), Vec(20, 0, 0)),
                ldraw_file='63864.dat')
PLATE1X4 = Brick('plate 1x3', 3710,
                 (Vec(-30, 0, 0), Vec(-10, 0, 0), Vec(10, 0, 0), Vec(30, 0, 0)),
                 ldraw_file='3710.dat')
TILE1X4 = Brick('tile 1x3', 2431,
                (Vec(-30, 0, 0), Vec(-10, 0, 0), Vec(10, 0, 0), Vec(30, 0, 0)),
                ldraw_file='2431.dat')
PLATE2X2 = Brick('plate 2x2', 3022,
                 (Vec(-10, 0, 10), Vec(10, 0, 10),
                  Vec(-10, 0, -10), Vec(10, 0, -10)),
                 ldraw_file='3022.dat')
TILE2X2 = Brick('tile 2x2', 3068,
                (Vec(-10, 0, 10), Vec(10, 0, 10),
                 Vec(-10, 0, -10), Vec(10, 0, -10)),
                ldraw_file='3068b.dat')
PLATE2X3 = Brick('plate 2x3', 3021,
                 (Vec(-20, 0, 10), Vec(0, 0, 10), Vec(20, 0, 10),
                  Vec(-20, 0, -10), Vec(0, 0, -10), Vec(20, 0, -10)),
                 ldraw_file='3021.dat')
CORNER2X2 = Brick('corner 2x2', 2420,
                  (Vec(0, 0, 0), Vec(0, 0, 20), Vec(20, 0, 0)),
                  ldraw_file='2420.dat')
