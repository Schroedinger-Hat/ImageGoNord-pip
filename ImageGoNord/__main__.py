#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Standard python module
import sys
import argparse

from ImageGoNord import NordPaletteFile
from ImageGoNord import GoNord

parser_image_go_nord = argparse.ArgumentParser(
    prog="image-go-nord",
    add_help=True,
)

parser_image_go_nord.add_argument(
    "-f",
    dest="force",
    action="store_true",
    help="If a file descriptor for a destination file cannot be obtained, as described in step 3.a.ii., attempt to "
    "unlink the destination file and proceed.",
)

parser_image_go_nord.add_argument(
    "-i",
    dest="interactive",
    action="store_true",
    help="Write a prompt to standard error before copying to any existing non-directory destination file.",
)

parser_image_go_nord.add_argument(
    "source_file",
    nargs="+",
    help="A pathname of a file to be copied. If a source_file operand is '-', it shall refer to a file named -; "
    "implementations shall not treat it as meaning standard input. target_file",
)

parser_image_go_nord.add_argument(
    "target_file",
    help="A pathname of an existing or nonexistent file, used for the output when a single file is copied. If a "
    "target_file operand is '-', it shall refer to a file named -; implementations shall not treat it as meaning "
    "standard output.",
)


def main():

    args = parser_image_go_nord.parse_args(sys.argv[1:])


    # E.g. Replace pixel by pixel
    # go_nord = GoNord()
    # image = go_nord.open_image("images/test.jpg")
    # go_nord.convert_image(image, save_path='images/test.processed.jpg')

    # E.g. Avg algorithm and less colors
    # go_nord.enable_avg_algorithm()
    # go_nord.reset_palette()
    # go_nord.add_file_to_palette(NordPaletteFile.POLAR_NIGHT)
    # go_nord.add_file_to_palette(NordPaletteFile.SNOW_STORM)

    # You can add color also by their hex code
    # go_nord.add_color_to_palette('#FF0000')
    #
    # image = go_nord.open_image("images/test.jpg")
    # go_nord.convert_image(image, save_path='images/test.avg.jpg')

    # E.g. Resized img no Avg algorithm and less colors
    # go_nord.disable_avg_algorithm()
    # go_nord.reset_palette()
    # go_nord.add_file_to_palette(NordPaletteFile.POLAR_NIGHT)
    # go_nord.add_file_to_palette(NordPaletteFile.SNOW_STORM)

    # image = go_nord.open_image("images/test.jpg")
    # resized_img = go_nord.resize_image(image)
    # go_nord.convert_image(resized_img, save_path='images/test.resized.jpg')

    # E.g. Quantize

    # image = go_nord.open_image("images/test.jpg")
    # go_nord.reset_palette()
    # go_nord.set_default_nord_palette()
    # quantize_image = go_nord.quantize_image(image, save_path='images/test.quantize.jpg')

    # To base64
    # go_nord.image_to_base64(quantize_image, 'jpeg')


if __name__ == "__main__":
    sys.exit(main())
