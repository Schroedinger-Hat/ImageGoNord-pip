#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse

# from torch.fx.experimental.unification.multipledispatch.dispatcher import source

from ImageGoNord import NordPaletteFile
from ImageGoNord import GoNord

parser_image_go_nord = argparse.ArgumentParser(
    prog="image-go-nord",
    add_help=True,
    description="A tool to convert any RGB image or video to any theme or color palette input by the user. "
    "By default the algorithm is pixel-by-pixel and will be disable by --avg or --ai usage.",
)

parser_image_go_nord.add_argument(
    "--avg",
    dest="avg",
    action="store_true",
    default=False,
    help="enable avg algorithm and less colors, if not enable the default is pixel-by-pixel approach, "
    "note: that option is disable by --ai usage.",
)

parser_image_go_nord.add_argument(
    "--ai",
    dest="ai",
    action="store_true",
    default=False,
    help="process image by using a PyTorch model 'PaletteNet' for recoloring the image, "
    "note: that disable pixel-by-pixel and avg algorithms.",
)

parser_image_go_nord.add_argument(
    "--blur",
    dest="blur",
    action="store_true",
    default=False,
    help="enable blur",
)

parser_image_go_nord.add_argument(
    "--quantize",
    dest="quantize",
    action="store_true",
    default=False,
    help="enable quantization digital image processing, it reduces the number of distinct colors in "
    "an image while maintaining its overall visual quality.",
)

parser_image_go_nord.add_argument(
    "--base64",
    dest="base64",
    action="store_true",
    default=False,
    help="enable base64 convertion during processing phase.",
)

parser_image_go_nord.add_argument(
    "--resize",
    dest="size",
    nargs=2,
    type=int,
    metavar=("WEIGHT", "HEIGHT"),
    default=None,
    help="resize the image during pre-processing phase.",
)

parser_image_go_nord.add_argument(
    "--reset-palette",
    dest="reset_palette",
    action="store_true",
    default=False,
    help="reset the palette to zero color, you can add colors with multiple --add ADD calls.",
)

parser_image_go_nord.add_argument(
    "--add",
    dest="add",
    action="append",
    default=[],
    help="add color by hex16 code '#FF0000', name: 'AURORA', 'FROST', 'POLAR_NIGHT', 'SNOW_STORM' "
    "or an existing file path it contain a color palette, one hex base 16 peer line ex: #FFFFFF . "
    "note: --add ADD can be call more of one time, no trouble to mixe them.",
)

parser_image_go_nord.add_argument(
    "-i",
    "--interactive",
    dest="interactive",
    action="store_true",
    default=False,
    help="write a prompt for confirmation about: start processing, overwrite a existing file, by default no "
    "questions is asking. note: during prompt if response is 'N', a filename will be found automatically.",
)

parser_image_go_nord.add_argument(
    "-y",
    "--yes",
    dest="yes",
    action="store_true",
    default=False,
    help="automatically by pass question by confirm with 'Y', that mean yes to continue and yes to "
    "overwrite existing files, note: by default prompt questions.",
)

parser_image_go_nord.add_argument(
    "source",
    nargs=argparse.ONE_OR_MORE,
    default=None,
    metavar="SOURCE",
    help="a pathname of an existing file or directory, note: you can chain source "
    "like SOURCE [SOURCE ...] in that case TARGET will be consider as directory.",
)

parser_image_go_nord.add_argument(
    "target",
    nargs=1,
    default=None,
    metavar="TARGET",
    help="a pathname of an existing or nonexistent file or directory, note: if nonexistent TARGET "
    "finish by '/' or '\\' it will be consider as directory and will be create if necessary. "
    "(no panik if the directory all ready exist it will be use as expected, in that "
    "case '/' or '\\' is optional).",
)


class ImageGoNordCLI:
    def __init__(self, **kwargs):
        self.go_nord = GoNord()

        self.blur = kwargs.get("blur", None)
        self.avg = kwargs.get("avg", None)
        self.ai = kwargs.get("ai", None)
        self.quantize = kwargs.get("quantize", None)
        self.base64 = kwargs.get("base64", None)
        self.reset_palette = kwargs.get("reset_palette", None)
        self.add = kwargs.get("add", None)

        self.__size = None
        self.size = kwargs.get("size", None)

        self.interactive = kwargs.get("interactive", None)
        self.yes = kwargs.get("yes", None)

        self.target_directory = None
        self.target_file = None

        self.__source = None
        self.source = kwargs.get("source", None)

        self.__target = None
        self.target = kwargs.get("target", None)

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        if value:
            value = tuple(value)
        if self.size != value:
            self.__size = value

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, value):
        if isinstance(value, list):
            source_list = []
            for src in value:
                # Reset src_to_use value each iteration
                if isinstance(src, str):
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

                # Links and dead links is supported
                src_to_use = self.lookup_file(src_to_use)

                # That is a file
                if os.path.isfile(src_to_use):
                    if (
                        self.lookup_file_supported_input_format(src_to_use)
                        and src_to_use not in source_list
                    ):
                        source_list.append(src_to_use)

                # That is a directory
                elif os.path.isdir(src_to_use):

                    # Check recursively for supported input file
                    for root, _, files in os.walk(src_to_use):
                        for file in files:
                            if (
                                self.lookup_file_supported_input_format(file)
                                and os.path.join(root, file) not in source_list
                            ):
                                source_list.append(os.path.join(root, file))

            if self.source != source_list:
                self.__source = source_list
        else:
            self.__source = []

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        if isinstance(value, str):
            if (
                len(self.source) > 1
                or len(self.source) == 1 and value.endswith(os.sep)
                or len(self.source) == 1 and value == "."
                or len(self.source) == 1 and value == ".."
            ):
                if os.path.exists(value):
                    value = os.path.realpath(value)
                else:
                    value = os.path.abspath(value)
                self.target_directory = value
                self.target_file = None
            elif len(self.source) == 1 and not value.endswith(os.sep):
                if os.path.exists(value):
                    value = self.lookup_file(value)
                else:
                    value = os.path.abspath(value)
                self.target_directory = None
                self.target_file = value
            else:
                value = None
                self.target_directory = None
                self.target_file = None

        else:
            value = None
            self.target_directory = None
            self.target_file = None

        if self.target != value:
            self.__target = value

    @staticmethod
    def lookup_file(path):
        if os.path.islink(path):
            while os.path.islink(path):
                path = os.readlink(path)
        if os.path.exists(path):
            return os.path.realpath(path)
        return None

    def lookup_file_supported_input_format(self, path):
        _, __, f_ext = self.lookup_file_into(path)
        # Match each file PIL input image format by extension name
        if f_ext.lower()[1:] in [
            "gif",
            "jpg",
            "jpeg",
            "png",
            "bmp",
            "tiff",
            "blp",
        ]:
            return True
        return False

    @staticmethod
    def lookup_file_into(path):
        basedir = os.path.dirname(path)
        f_name, f_ext = os.path.splitext(os.path.basename(path).split("/")[-1])
        return basedir, f_name, f_ext

    def lookup_file_get_next_non_existing_filename(self, path):
        basedir, f_name, f_ext = self.lookup_file_into(path)
        if self.interactive is False and self.yes is False:
            if os.path.exists(path):
                count = 1
                while os.path.exists(f"{os.path.join(basedir, f_name)}-{count}{f_ext}"):
                    count += 1  # pragma: no cover
                return f"{os.path.join(basedir, f_name)}-{count}{f_ext}"
            return path
        elif self.interactive is True and self.yes is False:  # pragma: no cover
            if os.path.exists(path):
                if self.ask_to_continue(f"File all ready exist: {path}? (Y/n) "):
                    return path
                else:
                    count = 1
                    while os.path.exists(
                        f"{os.path.join(basedir, f_name)}-{count}{f_ext}"
                    ):
                        count += 1
                    return f"{os.path.join(basedir, f_name)}-{count}{f_ext}"
            return path
        return path

    @staticmethod
    def ask_to_continue(text: str, startswith: str = "N"):

        if not input(f"{text}").upper().startswith(startswith):
            return True
        return False


    def print_summary(self):
        # header
        sys.stdout.write("\n")
        try:
            sys.stdout.write(
                f"{' IMAGE GO NORD SUMMARY '.center(os.get_terminal_size().columns, '=')}\n"
            )   # pragma: no cover
        except OSError:
            sys.stdout.write(
                f"{' IMAGE GO NORD SUMMARY '.center(80, '=')}\n"
            )

        # setting
        sys.stdout.write(
            f"Pixel-by-Pixel: {False if self.avg or self.ai else True}\n"
            f"AVG: {self.avg}\n"
            f"AI: {self.ai}\n"
            f"Blur: {self.blur}\n"
            f"Quantize: {self.quantize}\n"
            f"Base64: {self.base64}\n"
            f"Resize: {self.size}\n"
            f"Reset Palette: {self.reset_palette}\n"
            f"Interactive: {self.interactive}\n"
            f"Yes: {self.yes}\n"
        )

        # Palette
        # colors from add
        sys.stdout.write("Add color: ")
        if self.add:
            sys.stdout.write("\n")
            for add in self.add:
                sys.stdout.write(f"\t{add}\n")
        else:
            sys.stdout.write("None\n")

        # colors from go_nord point of view
        sys.stdout.write(f"Color{'s' if len(self.source)>1 else ''}: ")
        if self.go_nord.get_palette_data():
            sys.stdout.write("\n")
            for hex16, rgb in self.go_nord.get_palette_data().items():
                sys.stdout.write(
                    f"\tHex: #{hex16}, RGB: ({rgb[0]},{rgb[1]},{rgb[2]})\n"
                )
        else:
            sys.stdout.write("None\n")

        # source
        sys.stdout.write(f"Source{'s' if len(self.source) > 1 else ''}:")
        if len(self.source) > 1:
            sys.stdout.write("\n")
            for source in self.source:
                sys.stdout.write(f"\t{source}\n")
        elif len(self.source) == 1:
            sys.stdout.write(f" {self.source[0]}\n")
        else:
            sys.stdout.write(f" None\n")

        # target
        if self.target_directory:
            sys.stdout.write(f"Target directory: {self.target_directory}\n")
        elif self.target_file:
            sys.stdout.write(f"Target file: {self.target_file}\n")
        else:
            sys.stdout.write(f"Target: {self.target}\n")

        # footer
        try:
            sys.stdout.write(f"{''.center(os.get_terminal_size().columns, '=')}\n")  # pragma: no cover
        except OSError:
            sys.stdout.write(f"{''.center(80, '=')}\n")

        sys.stdout.flush()

    def pre_processing_palette(self):
        if self.reset_palette:
            self.go_nord.reset_palette()

        for color in self.add:

            # You can add color also by their hex code
            if f"{color}".startswith("#") and len(f"{color}") == 7:
                self.go_nord.add_color_to_palette(color)

            # Here we can consider the name is a path of a filename to load
            if os.access(color, os.F_OK, follow_symlinks=True):
                with open(color) as file_to_import:
                    for line in file_to_import:
                        if f"{line}".startswith("#") and len(f"{line}".strip()) == 7:
                            self.go_nord.add_color_to_palette(f"{line}".strip())

            # You can add color also by their name
            if f"{color}" in ["AURORA", "FROST", "POLAR_NIGHT", "SNOW_STORM"]:
                self.go_nord.add_file_to_palette(getattr(NordPaletteFile, f"{color}"))

        # The end of the world
        if len(self.go_nord.get_palette_data()) == 0:
            sys.stdout.write("No color is load at all\n")
            return 1

        return 0

    def pre_processing(self):
        if self.avg:
            self.go_nord.enable_avg_algorithm()
        else:
            self.go_nord.disable_avg_algorithm()

        if self.blur:
            self.go_nord.enable_gaussian_blur()
        else:
            self.go_nord.disable_gaussian_blur()

    def processing(self):
        if self.source:
            try:
                sys.stdout.write(f"{''.center(os.get_terminal_size().columns, '=')}\n") # pragma: no cover
            except OSError:
                sys.stdout.write(f"{''.center(80, '=')}\n")
            sys.stdout.write("Processing\n")
            sys.stdout.flush()
            for src_path in self.source:

                # create directories if not exist
                if self.target_directory and not os.path.exists(self.target_directory):
                    os.makedirs(self.target_directory)
                if self.target_file and not os.path.exists(
                    os.path.dirname(self.target_file)
                ):
                    os.makedirs(os.path.dirname(self.target_file))

                # we use target var and not controlled target_directory or target_file vars,
                # that let the power to the end user by let him break everything.
                if os.path.isdir(self.target):
                    dst_path = self.lookup_file_get_next_non_existing_filename(
                        os.path.join(self.target, os.path.basename(src_path))
                    )
                else:
                    dst_path = self.lookup_file_get_next_non_existing_filename(
                        self.target
                    )

                # load the image inside the go_nord
                image = self.go_nord.open_image(src_path)

                # deal with size and send back result into image var
                if self.size:
                    resized_img = self.go_nord.resize_image(image, size=self.size)
                else:
                    resized_img = image

                sys.stdout.write(f"Convert {src_path} to {dst_path}\n")
                sys.stdout.flush()

                if dst_path:
                    if self.ai:
                        returned_image = self.go_nord.convert_image_by_model(
                            resized_img
                        )
                        self.go_nord.save_image_to_file(returned_image, dst_path)
                    else:

                        if self.quantize and not self.base64:
                            quantize_image = self.go_nord.quantize_image(
                                resized_img, save_path=dst_path
                            )
                            self.go_nord.save_image_to_file(quantize_image, dst_path)
                        # elif self.quantize and self.base64:
                        #     basedir, f_name, f_ext = self.lookup_file_into(dst_path)
                        #     quantize_image = self.go_nord.quantize_image(resized_img, save_path=dst_path)
                        #     self.go_nord.image_to_base64(quantize_image, f_ext[1:])
                        # elif not self.quantize and self.base64:
                        #     basedir, f_name, f_ext = self.lookup_file_into(dst_path)
                        #     self.go_nord.image_to_base64(resized_img, f_ext[1:])
                        else:
                            self.go_nord.convert_image(resized_img, save_path=dst_path)

        else:
            sys.stdout.write("Nothing to process\n")
        sys.stdout.flush()

    def post_processing(self):
        pass


    def run(self):   # pragma: no cover
        self.pre_processing()

        if self.pre_processing_palette():
            sys.stdout.write("Trouble during color palette initialize\n")
            return 1

        # The user have the control
        self.print_summary()
        if self.yes is False:
            sys.stdout.flush()
            if not self.ask_to_continue("Do you want to continue ? (Y/n) "):
                sys.stdout.write("All operations are stop by the user\n")
                sys.stdout.flush()
                return 0

        try:
            self.processing()
            self.post_processing()
        except KeyboardInterrupt:
            sys.stdout.write("All operations are interrupted by the user\n")

        # If we are here that because all is finish, we can exit with
        return 0


def main(): # pragma: no cover
    args = parser_image_go_nord.parse_args(sys.argv[1:])
    if args.base64:
        sys.stdout.write("base64 support is not supported\n")
        return 1

    cli = ImageGoNordCLI(
        ai=args.ai,
        blur=args.blur,
        avg=args.avg,
        quantize=args.quantize,
        base64=args.base64,
        reset_palette=args.reset_palette,
        add=args.add,
        size=args.size,
        interactive=args.interactive,
        yes=args.yes,
        source=args.source,
        target=args.target[0],
    )
    return cli.run()


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
