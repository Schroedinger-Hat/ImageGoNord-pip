import base64
import os
from io import BytesIO

from math import ceil

import threading

from PIL import Image, ImageFilter

from ImageGoNord.utility.quantize import quantize_to_palette
import ImageGoNord.utility.palette_loader as pl
from ImageGoNord.utility.ConvertUtility import ConvertUtility


class NordPaletteFile:
    """
    A class used to map the nord color-scheme into files.
    Each file contains the hex of colors

    ...

    Attributes
    ----------
    AURORA : str
        Aurora color-palette
    FROST : str
        Frost color-palette
    POLAR_NIGHT : str
        Polar night color-palette
    SNOW_STORM : str
        Snow Storm color-palette

    """

    AURORA = "Aurora.txt"
    FROST = "Frost.txt"
    POLAR_NIGHT = "PolarNight.txt"
    SNOW_STORM = "SnowStorm.txt"


class GoNord(object):
    """
    A class used for converting image to the nord palette
    It can be used also for converting image to other palette by loading different palette

    This class need Pillow and apply 3 different palette conversion algorithm:
        - replace pixel by avg area pixel
        - replace pixel by pixel
        - apply a filter by using pillow features

    Attributes
    ----------
    PALETTE_LOOKUP_PATH : str
        path to look for finding the palette files (.txt)
    USE_GAUSSIAN_BLUR : bool
        enable or disable the blur (in output)
    USE_AVG_COLOR : bool
        enable or disable avg algorithm
    AVG_BOX_DATA : dict
        params (width and height) of the avg area to be considered
    AVAILABLE_PALETTE : list
        loaded palette list
    PALETTE_DATA : dict
        available palette data in hex : rgb format

    Methods
    -------
    set_palette_lookup_path(self, path)
        Set the base_path for the palette folder

    set_default_nord_palette(self)
        Set available palette as the default palette

    get_palette_data(self)
        Build the palette data from configuration

    add_color_to_palette(self, hex_color)
        Add hex color to current palette

    reset_palette(self)
        Reset the available_palette prop

    add_file_to_palette(self, file)
        Append a custom file to the available palette

    enable_gaussian_blur(self)
        Enable blur filter

    disable_gaussian_blur(self)
        disabled blur filter

    open_image(self, path)
        Load an image using Pillow utility

    resize_image(self, image, w=0, h=0)
        Resize an image using Pillow utility

    image_to_base64(self, image, extension)
        Convert a Pillow image to base64 string

    base64_to_image(self, img_b64)
        Convert a base64 string to a Pillow image

    load_pixel_image(self, opened_image)
        Load the pixel map of a given Pillow image

    enable_avg_algorithm(self)
        Enable avg algorithm

    disable_avg_algorithm(self)
        Disabled avg algorithm

    set_avg_box_data(self, w=-2, h=3)
        Set the dimension of the AVG area box to use

    quantize_image(self, image, save_path='')
        Quantize a Pillow image by applying the available palette

    convert_image(self, image, palettedata, save_path='')
        Process a Pillow image by replacing pixel or by avg algorithm

    save_image_to_file(self, image, path)
        Save a Pillow image to file
    """

    DEFAULT_PALETTE_PATH = '../palettes/Nord/'

    if (os.path.exists('../palettes/Nord/') == False):
        DEFAULT_PALETTE_PATH = 'ImageGoNord/palettes/Nord/'

    PALETTE_LOOKUP_PATH = DEFAULT_PALETTE_PATH
    USE_GAUSSIAN_BLUR = False
    USE_AVG_COLOR = False
    AVG_BOX_DATA = {"w": -2, "h": 3}
    TRANSPARENCY_TOLERANCE = 190
    MAX_THREADS = 10

    AVAILABLE_PALETTE = []
    PALETTE_DATA = {}

    def __init__(self):
        """Constructor: init variables & config"""
        self.set_default_nord_palette()
        self.set_avg_box_data()

    def set_palette_lookup_path(self, path):
        """Set the base_path for the palette folder"""
        self.PALETTE_LOOKUP_PATH = path

    def set_default_nord_palette(self):
        """Set available palette as the default palette"""
        self.AVAILABLE_PALETTE = [
            NordPaletteFile.POLAR_NIGHT,
            NordPaletteFile.SNOW_STORM,
            NordPaletteFile.FROST,
            NordPaletteFile.AURORA,
        ]

    def get_palette_data(self):
        """
        Build the palette data from configuration

        Returns
        -------
        dict
            The palette data: keys are hex color code, values are rgb values
        """
        for palette_file in self.AVAILABLE_PALETTE:
            hex_colors = pl.import_palette_from_file(
                self.PALETTE_LOOKUP_PATH + palette_file)
            for hex_color in hex_colors:
                self.PALETTE_DATA[hex_color] = pl.export_tripletes_from_color(
                    hex_color)

        # Delete empty lines, if they exist.
        if self.PALETTE_DATA.get('') and len(self.PALETTE_DATA['']) == 0:
            del self.PALETTE_DATA['']

        return self.PALETTE_DATA

    def add_color_to_palette(self, hex_color):
        self.PALETTE_DATA[hex_color[1:]] = pl.export_tripletes_from_color(hex_color[1:])

    def reset_palette(self):
        """Reset available palette array"""
        self.AVAILABLE_PALETTE = []
        self.PALETTE_DATA = {}

    def add_file_to_palette(self, file):
        """Method for adding file to the available palette"""
        self.AVAILABLE_PALETTE.append(file)
        self.get_palette_data()

    def set_transparency_tolerance(self, tolerance):
        """Method for changing the alpha tolerance"""
        self.TRANSPARENCY_TOLERANCE = int(tolerance)

    def enable_gaussian_blur(self):
        """Enable gaussian blur on the output img"""
        self.USE_GAUSSIAN_BLUR = True

    def disable_gaussian_blur(self):
        """Disable gaussian blur on the output img"""
        self.USE_GAUSSIAN_BLUR = False

    def open_image(self, path):
        """
        Load an image using Pillow utility

        Parameters
        ----------
        path : str
            the path and the filename where to save the image

        Returns
        -------
        pillow image
            opened image
        """
        opened_image = Image.open(path)
        if (type(opened_image.getpixel((0,0))) == int):
            opened_image = opened_image.convert('RGB')

        return opened_image

    def resize_image(self, image, size=(0, 0)):
        """
        Resize an image using Pillow utility

        Parameters
        ----------
        image : pillow image
            The source pillow image

        :param size:
            (width, height) of returning image, using half image size if not specified

        Returns
        -------
        pillow image
            resized image
        """

        if len(size) == 2 and all(size):
            return image.resize(size)

        w, h = image.size
        half_size = (round(w / 2), round(h / 2))
        return image.resize(half_size)

    def image_to_base64(self, image, extension):
        """
        Convert a Pillow image to base64 string

        Available extension: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html

        Parameters
        ----------
        image : pillow image
            The source pillow image
        extension : str
            The extension of the source image (mandatory)

        Returns
        -------
        pillow image
            processed image
        """
        im_file = BytesIO()
        image.save(im_file, format=extension)
        im_bytes = im_file.getvalue()
        return base64.b64encode(im_bytes)

    def base64_to_image(self, img_b64):
        """
        Convert a base64 string to a Pillow image

        Parameters
        ----------
        img_b64 : str
            The base64 string representation of the image

        Returns
        -------
        pillow image
            The converted image from base64
        """
        im_bytes = base64.b64decode(img_b64)
        im_file = BytesIO(im_bytes)
        return self.open_image(im_file)

    def load_pixel_image(self, opened_image):
        """
        Load the pixel map of a given Pillow image

        Parameters
        ----------
        image : pillow image
            The source pillow image

        Returns
        -------
        pillow image
            pixel map of the opened image
        """
        return opened_image.load()

    def enable_avg_algorithm(self):
        """
        Enabled avg algorithm

        """
        self.USE_AVG_COLOR = True

    def disable_avg_algorithm(self):
        """
        Disabled avg algorithm

        """
        self.USE_AVG_COLOR = False

    def set_avg_box_data(self, w=-2, h=2):
        """
        Set the dimension of the AVG area box to use

        Parameters
        ----------
        w : int
            Box's width
        h : int
            Box's height

        """
        self.AVG_BOX_DATA['w'] = w
        self.AVG_BOX_DATA['h'] = h

    def quantize_image(self, image, fill_color='2E3440', save_path=''):
        """
        Quantize a Pillow image by applying the available palette

        Parameters
        ----------
        image : pillow image
            The source pillow image
        fill_color: str
            Default fill color as foreground
        save_path : str, optional
            the path and the filename where to save the image

        Returns
        -------
        pillow image
            quantized image
        """

        data_colors = pl.create_data_colors(self.get_palette_data())
        while len(data_colors) < 768:
            data_colors.extend(pl.export_tripletes_from_color(fill_color))

        palimage = Image.new('P', (1, 1))
        palimage.putpalette(data_colors)
        quantize_img = quantize_to_palette(image, palimage)

        if (save_path != ''):
            self.save_image_to_file(quantize_img, save_path)

        return quantize_img

    def converted_loop(self, is_rgba, pixels, original_pixels, maxRow, maxCol, minRow=0, minCol=0):
        color_checked = {}
        for row in range(minRow, maxRow, 1):
            for col in range(minCol, maxCol, 1):
                try:
                    color_to_check = pixels[row, col]
                except Exception:
                    continue

                if (is_rgba):
                    if (color_to_check[3] < self.TRANSPARENCY_TOLERANCE):
                        continue

                if self.USE_AVG_COLOR == True:
                    # todo: improve this feature in performance
                    color_to_check = ConvertUtility.get_avg_color(
                        pixels=original_pixels, row=row, col=col, w=self.AVG_BOX_DATA['w'], h=self.AVG_BOX_DATA['h'])

                # saving in memory every checked color to improve performance
                key_color_checked = ','.join(str(e) for e in list(color_to_check))
                if (key_color_checked in color_checked):
                    difference = color_checked[key_color_checked]
                else:
                    differences = [[ConvertUtility.color_difference(color_to_check, target_value), target_name]
                                   for target_name, target_value in self.PALETTE_DATA.items()]
                    differences.sort()
                    difference = differences[0][1]

                color_checked[key_color_checked] = difference
                colors_list = self.PALETTE_DATA[difference]
                if (is_rgba and len(colors_list) == 3):
                    colors_list.append(color_to_check[3])

                pixels[row, col] = tuple(colors_list)
        return pixels

    def convert_image(self, image, save_path='', parallel_threading=False):
        """
        Process a Pillow image by replacing pixel or by avg algorithm

        Parameters
        ----------
        image : pillow image
            The source pillow image
        save_path : str, optional
            the path and the filename where to save the image

        Returns
        -------
        pillow image
            processed image
        """
        self.get_palette_data()
        original_image = image.copy()
        original_pixels = self.load_pixel_image(original_image)
        original_image.close()
        pixels = self.load_pixel_image(image)
        is_rgba = (image.mode == 'RGBA')
        if (parallel_threading == False):
            self.converted_loop(is_rgba, pixels, original_pixels, image.size[0], image.size[1])
        else:
            step = ceil(image.size[0] / self.MAX_THREADS)
            threads = []
            for row in range(step, image.size[0] + step, step):
                args = (is_rgba, pixels, original_pixels, row, image.size[1], row - step, 0)
                t = threading.Thread(target=self.converted_loop, args=args)
                t.daemon = True
                t.start()
                threads.append(t)

            for t in threads:
                t.join(timeout=30)

        if (self.USE_GAUSSIAN_BLUR == True):
            image = image.filter(ImageFilter.GaussianBlur(1))

        if (save_path != ''):
            self.save_image_to_file(image, save_path)

        return image

    def save_image_to_file(self, image, path):
        """
        Save a Pillow image to file

        Parameters
        ----------
        image : pillow image
            The source pillow image
        path : str
            the path and the filename where to save the image
        """
        image.save(path)
