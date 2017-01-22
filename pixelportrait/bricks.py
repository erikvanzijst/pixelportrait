from pixelportrait.lpp import Brick, Vec

PLATE1X1 = Brick('plate 1x1', 3024, (Vec(0, 0),), ldraw_file='3024.dat')
PLATE1X2 = Brick('plate 2x1', 3023, (Vec(-10, 0), Vec(10, 0)),
                 ldraw_file='3023.dat')
PLATE1X3 = Brick('plate 1x3', 3623, (Vec(-20, 0), Vec(0, 0), Vec(20, 0)),
                 ldraw_file='3623.dat')
PLATE1X4 = Brick('plate 1x3', 3710,
                 (Vec(-30, 0), Vec(-10, 0), Vec(10, 0), Vec(30, 0)),
                 ldraw_file='3710.dat')
PLATE2X2 = Brick('plate 2x2', 3022,
                 (Vec(-10, 10), Vec(10, 10),
                  Vec(-10, -10), Vec(10, -10)),
                 ldraw_file='3022.dat')
PLATE2X3 = Brick('plate 2x3', 3021,
                 (Vec(-20, 10), Vec(0, 10), Vec(20, 10),
                  Vec(-20, -10), Vec(0, -10), Vec(20, -10)),
                 ldraw_file='3021.dat')
CORNER2X2 = Brick('corner 2x2', 2420, [Vec(0, 0), Vec(0, 20), Vec(20, 0)],
                  ldraw_file='2420.dat')
