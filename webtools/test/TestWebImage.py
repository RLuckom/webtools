#!/usr/bin/env python

import os
from PIL import Image
import tempfile
import unittest

from webtools.WebImage import WebImage


class TestWebImage(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.big_img = Image.new('RGBA', (5000, 5000), (255, 0, 0))
        self.big_rect = Image.new('RGBA', (4000, 3000), (255, 0, 0))
        self.big_img_name = os.path.join(self.tmpdir, 'big_img.jpg')
        self.big_rect_name = os.path.join(self.tmpdir, 'big_rect.jpg')
        self.big_img.save(self.big_img_name)
        self.big_rect.save(self.big_rect_name)

    def test_scale_for_screens(self):
        img = WebImage(self.big_img_name)
        imgs = img._scale_for_screens()
        sizes = [i.size for i in imgs]
        self.assertSequenceEqual(sizes[0], (2160, 2160))
        img = WebImage(self.big_rect_name)
        imgs = img._scale_for_screens()
        sizes = [i.size for i in imgs]
        self.assertSequenceEqual(sizes[0], (40 * 72, 30 * 72))

    def test_save_sizes(self):
        img1 = WebImage(self.big_img_name)
        img2 = WebImage(self.big_rect_name)
        img1.save_multiple_sizes(save_dir=self.tmpdir)
        img2.save_multiple_sizes(save_dir=self.tmpdir)
        l = [os.path.basename(self.big_img_name),
             os.path.basename(self.big_rect_name),
             'SMALL', 'MED', 'BIG', 'THUMB']
        self.assertSequenceEqual(sorted(l), sorted(os.listdir(self.tmpdir)))

if __name__ == '__main__':
    unittest.main()
