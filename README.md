# Lego Pixel Portrait Generator

Takes an image file and converts it to a Lego mosaic.

## Usage

```
$ pip install -r requirements.txt
$ ./portrait.py < owen.png > owen.ldr
```

Mosaics are generated using the [LDraw](http://www.ldraw.org/) file format
which can be viewed using a variety of viewer applications, such as
[LDView](http://ldview.sourceforge.net/).

It can also be used as input for generating Lego instruction booklets.

![](https://bitbucket.org/evzijst/pixelportrait/raw/master/screenshot.jpg)

Images must be using 5 colors or less, as the Lego palette is rather limited.
