#!/usr/bin/env python

from collections import namedtuple
from PIL import Image
import os

Size = namedtuple('Size', ['x', 'y'])


class WebImage(object):
    '''Auto resizes images to fit four screen sizes, maintaining their
       original aspect ratio'''

    DEFAULT_PPI = 72
    DEFAULT_SCREENS = [Size(40, 30), Size(16, 12), Size(3, 5), Size(.5, .5)]

    def __init__(self, filename, **kwargs):
        '''Constructor

        The screens kwarg can be a set of four tuples of sizes in inches.
        The ppi kwarg can be an int representing desired resolution.
        Default ppi is 72.

        @param filename (str): full path to image.
        '''
        self.img = Image.open(filename)
        self._ppi = kwargs.get('ppi', self.DEFAULT_PPI)
        self._screens = [Size(*x) for x in kwargs.get('screens',
                                                      self.DEFAULT_SCREENS)]
        self._size_names = ['BIG', 'MED', 'SMALL', 'THUMB']

    def _scale_for_screens(self):
        '''Copies the image once for each of self's screens, and resizes
        each copy according to a screen

        @return (list) : list of resized images'''
        imgs = [self.img.resize(self._scale_to_screen(x), Image.ANTIALIAS)
                for x in self._screens]
        [img.info.__setitem__('dpi', self._ppi) for img in imgs]
        return imgs

    def _scale_to_screen(self, screen):
        '''Calculates the correct size to make the image fit within screen

        @param screen (Size namedtuple) : namedtuple (x, y) in inches
        @return (Size namedtuple) : namedtuple (x, y), resized, in pixels
        '''
        pixels = Size(screen.x * self._ppi, screen.y * self._ppi)
        x, y = self.img.size
        x_scale = 1 if x < pixels.x else pixels.x / float(x)
        y_scale = 1 if y < pixels.y else pixels.y / float(y)
        m = min(x_scale, y_scale)
        return Size(int(x * m), int(y * m))

    def save_multiple_sizes(self, save_dir=''):
        '''Saves BIG, MED, SMALL, and THUMB versions of the image in
        BIG, MED, SMALL, and THUMB subdirectories of save_dir.

        Sizes are set by the screens argument to __init__, or
        DEFAULT_SCREENS. Screen sizes are specified in inches, and
        converted to pixels internally. The screen size represents
        the largest allowable x and y dimensions; if the image is smaller
        than the screen size times the resolution, it will not be resized.
        The aspect ratio of the image will be preserved.

        @param save_dir (str) : path to directory in which to make
                                subdirectories for images.
        '''
        base, ext = os.path.splitext(os.path.basename(self.img.filename))
        imgs = self._scale_for_screens()
        dirs = [os.path.join(save_dir, x) for x in self._size_names]
        names = [base + '_' + x + ext for x in self._size_names]
        for img, dir, name in zip(imgs, dirs, names):
            if not os.path.exists(dir):
                os.makedirs(dir)
            img.save(os.path.join(dir, name))
