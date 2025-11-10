import unittest
from image_processing.image import RawImage

class TestRawImage(unittest.TestCase):

    def setUp(self):
        self.image = RawImage("./data/moon-u8be-3x2613x3900.raw", 3900, 2613, 3)

    def test_initialization(self):
        self.assertEqual(self.image.width, 3900)
        self.assertEqual(self.image.height, 2613)
        self.assertEqual(self.image.channel_nbr, 3)

    def test_get_set_pixel(self):
        self.image.set_value(0, 0, 0, 255)  # Set red channel at (0, 0)
        value = self.image.get_value(0, 0, 0)  # Get red channel at (0, 0)
        self.assertEqual(value, 255)

if __name__ == '__main__':
    unittest.main()
