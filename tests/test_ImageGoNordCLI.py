import os
import unittest
from io import StringIO
from unittest.mock import patch



from ImageGoNord.__main__ import ImageGoNordCLI

class TestImageGoNordCLI(unittest.TestCase):
    def setUp(self):
        self.cli = ImageGoNordCLI()
        self.images_directory = os.path.realpath(os.path.join(
            os.path.dirname(__file__),
            "..",
            "images"
        ))
        self.images_1 = os.path.realpath(os.path.join(
                os.path.dirname(__file__),
                "..",
                "images",
                "sh.png"
        ))
        self.images_2 = os.path.realpath(os.path.join(
            os.path.dirname(__file__),
            "..",
            "images",
            "test.jpg"
        ))

        if os.path.exists(os.path.join(os.path.dirname(__file__), "hello", "sh.png")):
            os.remove(os.path.join(os.path.dirname(__file__), "hello", "sh.png"))
            os.rmdir(os.path.join(os.path.dirname(__file__), "hello"))

    def tearDown(self):
        if os.path.exists(os.path.join(os.path.dirname(__file__), "hello", "sh.png")):
            os.remove(os.path.join(os.path.dirname(__file__), "hello", "sh.png"))
            os.rmdir(os.path.join(os.path.dirname(__file__), "hello"))


    def test_size(self):
        self.assertIsNone(self.cli.size)
        self.cli.size = [1920, 1080]
        self.assertEqual(self.cli.size, (1920, 1080))

    def test_source(self):
        self.assertEqual(self.cli.source, [])

        self.cli.source = [self.images_1, self.images_1]
        self.assertEqual(self.cli.source, [self.images_1])

        self.cli.source = None
        self.assertEqual(self.cli.source, [])

        self.cli.source = [self.images_1, self.images_2, None]
        self.assertEqual(self.cli.source, [self.images_1, self.images_2])

        self.cli.source = None
        self.assertEqual(self.cli.source, [])
        self.cli.source = [self.images_directory]
        self.assertTrue(self.images_1 in self.cli.source)
        self.assertTrue(self.images_2 in self.cli.source)

        self.cli.source = []
        self.assertEqual(self.cli.source, [])

    def test_target(self):
        self.cli.source = [self.images_1]

        self.assertIsNone(self.cli.target)
        self.cli.target = "./"

        self.assertEqual(self.cli.target , os.path.realpath(os.getcwd()))

        self.cli.target = "./hello42/"
        self.assertEqual(self.cli.target, os.path.realpath(os.path.join(os.getcwd(), "hello42")))
        self.assertIsNone(self.cli.target_file)
        self.assertEqual(self.cli.target_directory, os.path.realpath(os.path.join(os.getcwd(), "hello42")))

        self.cli.target = "./hello42"
        self.assertEqual(self.cli.target, os.path.realpath(os.path.join(os.getcwd(), "hello42")))
        self.assertIsNone(self.cli.target_directory)
        self.assertEqual(self.cli.target_file, os.path.realpath(os.path.join(os.getcwd(), "hello42")))

        self.cli.target = self.images_directory
        self.assertEqual(self.cli.target, os.path.realpath(os.path.join(os.getcwd(), self.images_directory)))
        self.assertIsNone(self.cli.target_directory)
        self.assertEqual(self.cli.target_file, os.path.realpath(os.path.join(os.getcwd(), self.images_directory)))

        self.cli.target = None
        self.assertIsNone(self.cli.target)
        self.assertIsNone(self.cli.target_directory)
        self.assertIsNone(self.cli.target_file)

        self.cli.source = None
        self.cli.target = ""
        self.assertIsNone(self.cli.target)
        self.assertIsNone(self.cli.target_directory)
        self.assertIsNone(self.cli.target_file)

    def test_lookup_file(self):
        self.assertEqual(self.cli.lookup_file("/dev/core"), "/proc/kcore")
        self.assertIsNone(self.cli.lookup_file("hello42"))

    def test_lookup_file_supported_input_format(self):
        self.assertTrue(self.cli.lookup_file_supported_input_format("image.jpg"))
        self.assertFalse(self.cli.lookup_file_supported_input_format("hello.42"))

    def test_lookup_file_into(self):
        basedir, f_name, f_ext = self.cli.lookup_file_into("/home/user/images/image1.jpg")
        self.assertEqual(basedir, "/home/user/images")
        self.assertEqual(f_name, "image1")
        self.assertEqual(f_ext, ".jpg")

    def test_lookup_file_get_next_non_existing_filename(self):
        self.cli.interactive = False
        self.cli.yes = False

        next_filename = os.path.realpath(os.path.join(
                os.path.dirname(__file__),
                "..",
                "images",
                "sh-1.png"
        ))
        self.assertEqual(
            self.cli.lookup_file_get_next_non_existing_filename(self.images_1),
            next_filename
        )
        file = os.path.join(
            os.getcwd(),
            "hello.42"
        )
        self.assertEqual(
            self.cli.lookup_file_get_next_non_existing_filename(file),
            file
        )


        self.cli.interactive = True
        self.cli.yes = True

        self.assertEqual(
            self.cli.lookup_file_get_next_non_existing_filename(self.images_1),
            self.images_1
        )

        self.cli.interactive = False
        self.cli.yes = True

        self.assertEqual(
            self.cli.lookup_file_get_next_non_existing_filename(self.images_1),
            self.images_1
        )

        # test interactive is a bit long to do because that is stdin and stdout in same time
        # with a write inside the stdin over a separate thread.

    def test_ask_to_continue(self):
        with patch('sys.stdin', StringIO('n\n')) as stdin, \
                patch('sys.stdout', new_callable=StringIO) as stdout:

            self.assertFalse(self.cli.ask_to_continue("Are you OK ? (Y/n) ", "N"))
            self.assertEqual( stdout.getvalue(), 'Are you OK ? (Y/n) ')
            self.assertEqual(stdin.read(), '')

        with patch('sys.stdin', StringIO('\n')) as stdin, \
                patch('sys.stdout', new_callable=StringIO) as stdout:

            self.assertTrue(self.cli.ask_to_continue("Are you OK ? (Y/n) ", "N"))
            self.assertEqual( stdout.getvalue(), 'Are you OK ? (Y/n) ')
            self.assertEqual(stdin.read(), '')

    def test_print_summary(self):
        with patch('sys.stdout', new_callable=StringIO) as stdout:
            expected = (
                f'\n'
                f'============================ IMAGE GO NORD SUMMARY =============================\n'
                f'Pixel-by-Pixel: True\n'
                f'AVG: None\n'
                f'AI: None\n'
                f'Blur: None\n'
                f'Quantize: None\n'
                f'Base64: None\n'
                f'Resize: None\n'
                f'Reset Palette: None\n'
                f'Interactive: None\n'
                f'Yes: None\n'
                f'Add color: None\n'
                f'Color: \n'
                f'\tHex: #2E3440, RGB: (46,52,64)\n'
                f'\tHex: #3B4252, RGB: (59,66,82)\n'
                f'\tHex: #434C5E, RGB: (67,76,94)\n'
                f'\tHex: #4C566A, RGB: (76,86,106)\n'
                f'\tHex: #D8DEE9, RGB: (216,222,233)\n'
                f'\tHex: #E5E9F0, RGB: (229,233,240)\n'
                f'\tHex: #ECEFF4, RGB: (236,239,244)\n'
                f'\tHex: #8FBCBB, RGB: (143,188,187)\n'
                f'\tHex: #88C0D0, RGB: (136,192,208)\n'
                f'\tHex: #81A1C1, RGB: (129,161,193)\n'
                f'\tHex: #5E81AC, RGB: (94,129,172)\n'
                f'\tHex: #BF616A, RGB: (191,97,106)\n'
                f'\tHex: #D08770, RGB: (208,135,112)\n'
                f'\tHex: #EBCB8B, RGB: (235,203,139)\n'
                f'\tHex: #A3BE8C, RGB: (163,190,140)\n'
                f'\tHex: #B48EAD, RGB: (180,142,173)\n'
                f'Source: None\n'
                f'Target: None\n'
                f'================================================================================\n'
            )
            self.cli.print_summary()
            self.assertEqual(stdout.getvalue(), expected)

        self.cli.source= [self.images_1]
        self.cli.target= self.images_2
        self.cli.go_nord.reset_palette()
        with patch('sys.stdout', new_callable=StringIO) as stdout:
            expected = (
                f'\n'
                f'============================ IMAGE GO NORD SUMMARY =============================\n'
                f'Pixel-by-Pixel: True\n'
                f'AVG: None\n'
                f'AI: None\n'
                f'Blur: None\n'
                f'Quantize: None\n'
                f'Base64: None\n'
                f'Resize: None\n'
                f'Reset Palette: None\n'
                f'Interactive: None\n'
                f'Yes: None\n'
                f'Add color: None\n'
                f'Color: None\n'
                f'Source: {self.images_1}\n'
                f'Target file: {self.images_2}\n'
                f'================================================================================\n'
            )
            self.cli.print_summary()
            self.assertEqual(stdout.getvalue(), expected)

        self.cli.source = None
        self.cli.target = os.getcwd()
        self.cli.add = ["#FFFFFF", "#OOOOOO",]
        with patch('sys.stdout', new_callable=StringIO) as stdout:
            expected = (
                f'\n'
                f'============================ IMAGE GO NORD SUMMARY =============================\n'
                f'Pixel-by-Pixel: True\n'
                f'AVG: None\n'
                f'AI: None\n'
                f'Blur: None\n'
                f'Quantize: None\n'
                f'Base64: None\n'
                f'Resize: None\n'
                f'Reset Palette: None\n'
                f'Interactive: None\n'
                f'Yes: None\n'
                f'Add color: \n'
                f'\t#FFFFFF\n'
                f'\t#OOOOOO\n'
                f'Color: None\n'
                f'Source: None\n'
                f'Target: None\n'
                f'================================================================================\n'
            )
            self.cli.print_summary()
            self.assertEqual(stdout.getvalue(), expected)

        self.cli.source = [self.images_directory]
        self.cli.target = os.getcwd()
        self.cli.add = []
        with patch('sys.stdout', new_callable=StringIO) as stdout:
            expected = (
                f'\n'
                f'============================ IMAGE GO NORD SUMMARY =============================\n'
                f'Pixel-by-Pixel: True\n'
                f'AVG: None\n'
                f'AI: None\n'
                f'Blur: None\n'
                f'Quantize: None\n'
                f'Base64: None\n'
                f'Resize: None\n'
                f'Reset Palette: None\n'
                f'Interactive: None\n'
                f'Yes: None\n'
                f'Add color: None\n'
                f'Colors: None\n'
                f'Sources:\n'
                f'\t{self.images_directory}/test-profile-ai-aurora.jpg\n'
                f'\t{self.images_directory}/test.resized.jpg\n'
                f'\t{self.images_directory}/test-profile.jpg\n'
                f'\t{self.images_directory}/test-average.jpg\n'
                f'\t{self.images_directory}/test-sh-ai.png\n'
                f'\t{self.images_directory}/test-profile-average.jpg\n'
                f'\t{self.images_directory}/test.jpg\n'
                f'\t{self.images_directory}/test-valley-ai.jpg\n'
                f'\t{self.images_directory}/sh.png\n'
                f'\t{self.images_directory}/valley.jpg\n'
                f'Target directory: {os.getcwd()}\n'
                f'================================================================================\n'
            )
            self.cli.print_summary()
            self.assertEqual(stdout.getvalue(), expected)

    def test_pre_processing_palette(self):
        # No colors at all
        self.cli.add = []
        self.cli.reset_palette = True
        self.assertEqual(1, self.cli.pre_processing_palette())

        # We got colors
        self.cli.add = [
            "#000000",
            "AURORA",
            os.path.join(os.path.dirname(__file__), "..", "ImageGoNord", "palettes", 'Nord', 'Frost.txt')
        ]
        self.cli.reset_palette = False
        self.assertEqual(0, self.cli.pre_processing_palette())

    def test_preprocessing(self):
        self.cli.blur = False
        self.cli.avg = False

        self.cli.pre_processing()
        self.assertFalse(self.cli.go_nord.USE_GAUSSIAN_BLUR)
        self.assertFalse(self.cli.go_nord.USE_AVG_COLOR)

        self.cli.blur = True
        self.cli.avg = True

        self.cli.pre_processing()
        self.assertTrue(self.cli.go_nord.USE_GAUSSIAN_BLUR)
        self.assertTrue(self.cli.go_nord.USE_AVG_COLOR)

    def test_processing(self):

        # Without setting
        self.cli.source = [self.images_1]
        self.cli.target = os.path.join(os.path.dirname(__file__), "hello", "sh.png")
        self.cli.add = []

        with (
            patch('sys.stdin', StringIO('n\n')) as stdin, \
            patch('sys.stdout', new_callable=StringIO) as stdout):
            expected = (
                f'================================================================================\n'
                f'Processing\n'
                f'Convert {self.images_1} to {os.path.join(os.path.dirname(__file__), "hello", "sh.png")}\n'
            )
            self.cli.processing()
            self.assertEqual(stdout.getvalue(), expected)

        if os.path.exists(os.path.join(os.path.dirname(__file__), "hello", "sh.png")):
            os.remove(os.path.join(os.path.dirname(__file__), "hello", "sh.png"))
            os.rmdir(os.path.join(os.path.dirname(__file__), "hello"))

        # test with directory target and resize
        self.cli.source = [self.images_1]
        self.cli.target = os.path.join(os.path.dirname(__file__), "hello/")
        self.cli.size = (48, 48)
        self.cli.add = []
        self.cli.processing()
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(__file__), "hello", "sh.png")))

        if os.path.exists(os.path.join(os.path.dirname(__file__), "hello", "sh.png")):
            os.remove(os.path.join(os.path.dirname(__file__), "hello", "sh.png"))
            os.rmdir(os.path.join(os.path.dirname(__file__), "hello"))

        # test ai
        self.cli.source = [self.images_1]
        self.cli.target = os.path.join(os.path.dirname(__file__), "hello/")
        self.cli.size = (48, 48)
        self.cli.add = []
        self.cli.ai = True
        self.cli.processing()
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(__file__), "hello", "sh.png")))

        if os.path.exists(os.path.join(os.path.dirname(__file__), "hello", "sh.png")):
            os.remove(os.path.join(os.path.dirname(__file__), "hello", "sh.png"))
            os.rmdir(os.path.join(os.path.dirname(__file__), "hello"))

        # test quantize
        self.cli.source = [self.images_1]
        self.cli.target = os.path.join(os.path.dirname(__file__), "hello/")
        self.cli.size = (48, 48)
        self.cli.add = []
        self.cli.ai = False
        self.cli.quantize = True
        self.cli.processing()
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(__file__), "hello", "sh.png")))

        if os.path.exists(os.path.join(os.path.dirname(__file__), "hello", "sh.png")):
            os.remove(os.path.join(os.path.dirname(__file__), "hello", "sh.png"))
            os.rmdir(os.path.join(os.path.dirname(__file__), "hello"))

        # Without source
        self.cli.source = None
        self.cli.target = None
        self.cli.ai = False
        self.cli.quantize = False
        self.cli.add = []

        with (patch('sys.stdout', new_callable=StringIO) as stdout):
            expected = (
                'Nothing to process\n'
            )
            self.cli.processing()
            self.assertEqual(stdout.getvalue(), expected)

    def test_post_processing(self):
        self.assertIsNone(self.cli.post_processing())


if __name__ == '__main__':
    unittest.main()
