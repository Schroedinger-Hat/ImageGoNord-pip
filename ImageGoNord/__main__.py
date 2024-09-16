#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

# Standard python module
import sys
import argparse

# from torch.fx.experimental.unification.multipledispatch.dispatcher import source

from ImageGoNord import NordPaletteFile
from ImageGoNord import GoNord

parser_image_go_nord = argparse.ArgumentParser(
    prog="image-go-nord",
    add_help=True,
    description="A tool to convert any RGB image or video to any theme or color palette input by the user",
)

parser_image_go_nord.add_argument(
    "--avg",
    dest="avg",
    action="store_true",
    default=False,
    help="Avg algorithm and less colors it not enable it will use pixel-by-pixel approach",
)

parser_image_go_nord.add_argument(
    "--blur",
    dest="blur",
    action="store_true",
    default=False,
    help="Enable",
)

parser_image_go_nord.add_argument(
    "--quantize",
    dest="quantize",
    action="store_true",
    default=False,
    help="Enable quantization digital image processing. That reduces the number of distinct colors in "
         "an image while maintaining its overall visual quality.",

)

parser_image_go_nord.add_argument(
    "--base64",
    dest="base64",
    action="store_true",
    default=False,
    help="Enable base64 convertion",
)

parser_image_go_nord.add_argument(
    "--reset-palette",
    dest="reset_palette",
    action="store_true",
    default=False,
    help="Rest the palette to zero color, you can add colors with multiple --add call",
)

parser_image_go_nord.add_argument(
    "--add",
    dest="add",
    action="append",
    help="Add color also by hex code ex: '#FF0000' or name ex: 'POLAR_NIGHT', 'SNOW_STORM', it option "
    "can be call more of one time",
)

parser_image_go_nord.add_argument(
    "-i",
    dest="interactive",
    action="store_true",
    default=False,
    help="Write a prompt for confirmation about: start processing, overwrite a existing file or create a target directory",
)

parser_image_go_nord.add_argument("source", nargs=argparse.ONE_OR_MORE, default=None)

parser_image_go_nord.add_argument(
    "target",
    nargs=1,
    default=None,
    help="A pathname of an existing or nonexistent file, used for the output when a single file is copied.",
)


class ImageGoNordCLI:
    def __init__(self, **kwargs):
        self.go_nord = GoNord()

        self.blur = kwargs.get("blur", None)
        self.avg = kwargs.get("avg", None)
        self.quantize = kwargs.get("quantize", None)
        self.base64 = kwargs.get("base64", None)
        self.reset_palette = kwargs.get("reset_palette", None)
        self.add = kwargs.get("add", None)

        self.interactive = kwargs.get("interactive", None)

        self.__source = None
        self.source = kwargs.get("source", None)

        self.__target = None
        self.target = kwargs.get("target", None)



    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, value):
        if value:
            source_list = []
            for src in value:
                # Reset src_to_use value each iteration
                if hasattr(src, "name"):
                    src_to_use = src.name
                elif isinstance(src, str):
                    src_to_use = src
                else:
                    src_to_use = None

                # Don't need to continue if path do not exist or cant be read
                if (
                    not src_to_use
                    or not os.access(src_to_use, os.F_OK, follow_symlinks=True)
                    or not os.access(src_to_use, os.R_OK, follow_symlinks=True)
                ):
                    continue

                # That is a file
                if os.path.isfile(src_to_use) and src_to_use not in source_list:
                    source_list.append(src_to_use)

                # That is a directory
                elif os.path.isdir(src_to_use):

                    # Check recursively
                    for root, dirs, files in os.walk(src_to_use):
                        for file in files:
                            # Match each file PIL input image format by extension name
                            for extension in [
                                "gif",
                                "GIF",
                                "Gif",
                                "jpg",
                                "JPG",
                                "Jpg",
                                "jpeg",
                                "JPEG",
                                "Jpeg",
                                "png",
                                "PNG",
                                "Png",
                                "bmp",
                                "BMP",
                                "Bmp",
                                "tiff",
                                "TIFF",
                                "Tif",
                                "blp",
                                "BLP",
                                "Blp",
                            ]:
                                if file.endswith(extension) and os.path.join(root, file) not in source_list:
                                    source_list.append(os.path.join(root, file))

            if self.source != source_list:
                self.__source = source_list
        else:
            self.__source = None

    def print_summary(self):
        sys.stdout.write(
            f"\n"
            f"{"| IMAGE GO NORD SUMMARY |".center(os.get_terminal_size().columns, "-")}\n"
            f"AVG: {self.avg}\n"
            f"Blur: {self.blur}\n"
            f"Quantize: {self.quantize}\n"
            f"Base64: {self.base64}\n"
            f"Reset Palette: {self.reset_palette}\n"
            f"Add color: {self.add}\n"
            
            f"\n"
        )

        if len(self.source) > 1:
            target_type = "directory"
            target_add_slash = "/"
            sys.stdout.write(f"Source files:\n")
            for source in self.source:
                sys.stdout.write(f"{source}\n")
        elif len(self.source) == 1:
            target_type = "file"
            target_add_slash = ""
            sys.stdout.write(f"Source file: {self.source[0]}\n")
        else:
            target_type = "FILE"
            target_add_slash = ""
            sys.stdout.write(f"Source: None\n")
        sys.stdout.write(
            f"\n"
            f"Target {target_type}: {self.target[0]}{target_add_slash}\n"
            f"\n"
            f"{"".center(os.get_terminal_size().columns, "-")}\n"
        )
        sys.stdout.flush()


    def pre_processing_palette(self):
        # --reset-palette
        if self.reset_palette:
            self.go_nord.reset_palette()

        # --add
        for color in self.add:

            # You can add color also by their hex code
            if f"{color}".startswith("#") and len(f"{color}") == 7:
                self.go_nord.add_color_to_palette('#FF0000')

            # You can add color also by their name
            if f"{color}" in ["AURORA", "FROST", "POLAR_NIGHT", "SNOW_STORM"]:
                self.go_nord.add_file_to_palette(getattr(NordPaletteFile, f"{color}"))

    def pre_processing(self):
        # --avg
        if self.avg:
            self.go_nord.enable_avg_algorithm()
        else:
            self.go_nord.disable_avg_algorithm()

        # --blur
        if self.blur:
            self.go_nord.enable_gaussian_blur()
        else:
            self.go_nord.disable_gaussian_blur()

    def ask_to_confinue(self):
        if self.interactive:
            if not input("do you want to continue ? (Y/n)").upper().startswith("Y"):
                return False
            return True

    def processing(self):
        pass
        # process
        # for image in self.source:
        #     self.go_nord.open_image(image)
        #     if self.base64:
        #         self.go_nord.image_to_base64(
        #             os.path.join(
        #                 self.target,
        #                 os.path.basename(image)
        #             )
        #         )
        #     else:
        #         self.go_nord.save_image_to_file(os.path.join(
        #                 self.target,
        #                 os.path.basename(image)
        #             )

    def post_processing(self):
        pass

    def run(self):
        self.pre_processing_palette()
        self.pre_processing()
        self.print_summary()
        if not self.ask_to_confinue():
            return 0
        self.processing()
        self.post_processing()



        # post processing


        # self.go_nord = GoNord()
        # if self.pixel_by_pixel:
        #
        #
        #     print(f"Convertion pixel-by-pixel {self.source_file.name} to {self.target_file}")
        #     image = self.go_nord.open_image(self.source_file.name)
        #     self.go_nord.convert_image(
        #         image,
        #         save_path=self.target_file
        #     )
        # --pixel-by-pixel
        # E.g. Replace pixel by pixel
        # go_nord = GoNord()
        # image = go_nord.open_image("images/test.jpg")
        # go_nord.convert_image(image, save_path='images/test.processed.jpg')
        return 0

    # --avg
    # E.g. Avg algorithm and less colors
    # go_nord.enable_avg_algorithm()
    # go_nord.reset_palette()
    # go_nord.add_file_to_palette(NordPaletteFile.POLAR_NIGHT)
    # go_nord.add_file_to_palette(NordPaletteFile.SNOW_STORM)

    # --add
    # You can add color also by their hex code
    # go_nord.add_color_to_palette('#FF0000')
    #
    # image = go_nord.open_image("images/test.jpg")
    # go_nord.convert_image(image, save_path='images/test.avg.jpg')



    # image = go_nord.open_image("images/test.jpg")
    # resized_img = go_nord.resize_image(image)
    # go_nord.convert_image(resized_img, save_path='images/test.resized.jpg')

    # E.g. Quantize
    # --quantize
    # image = go_nord.open_image("images/test.jpg")
    # go_nord.reset_palette()
    # go_nord.set_default_nord_palette()
    # quantize_image = go_nord.quantize_image(image, save_path='images/test.quantize.jpg')

    # To base64
    # --base64
    # go_nord.image_to_base64(quantize_image, 'jpeg')


def main():
    args = parser_image_go_nord.parse_args(sys.argv[1:])
    cli = ImageGoNordCLI(
        blur=args.blur,
        avg=args.avg,
        quantize=args.quantize,
        base64=args.base64,
        reset_palette=args.reset_palette,
        add=args.add,
        interactive=args.interactive,
        source=args.source,
        target=args.target,
    )
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())