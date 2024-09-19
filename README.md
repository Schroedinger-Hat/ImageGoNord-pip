# ImageGoNord - RGB image and video to any kind of palette or theme

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/image-go-nord)
[![PyPI](https://img.shields.io/pypi/v/image-go-nord)](https://pypi.org/project/image-go-nord/)
[![license](https://img.shields.io/badge/license-MIT-green)](https://github.com/Schrodinger-Hat/ImageGoNord-pip/blob/master/LICENSE)
[![Join the community on Spectrum](https://withspectrum.github.io/badge/badge.svg)](https://spectrum.chat/image-go-nord)

A tool that can convert your rgb images to nordtheme, gruvbox, catpuccin and many more palettes.
Video included.

This repository is a python package.

You can find a demo on [the website](https://ign.schrodinger-hat.it) for testing out the package.
The main repository of this whole project is [ImageGoNord](https://github.com/Schrodinger-Hat/ImageGoNord).

It's including an API layer, in case you'd like to set it up also for your project.

### Documentation

You can find the [documentation into this repository](https://github.com/Schrodinger-Hat/ImageGoNord-pip/tree/master/docs) and also on the website.
If you have any questions, please reach us at us@schrodinger-hat.it

### Inspiration

We are in love with Nordtheme, that is why we created this repository.

Our goal is to make a shortcut to convert anything into any kind of themes, by starting from the images and going to videos.
<br>An example could be an awesome wallpaper converted into the Nordtheme palette.

We checked the commnunity and we did not find anything similar or any project that can accomplish this task. So, here we are.

Of course, we resolved the issue for any kind of palette, theme and it's video supported.

### What you can do with this package

You can convert any image into the nord palette (or others). Here are some examples:

**Original**

[![Original](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/test.jpg)](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/test.jpg)


**Processed with avg algorithm**

[![Original](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/test-average.jpg)](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/test-average.jpg)


-----

**Original**

[![Original](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/test-profile.jpg)](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/test-profile.jpg)


**Processed with avg algorithm**

[![Original](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/test-profile-average.jpg)](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/test-profile-average.jpg)


### ImageGoNord with AI - PaletteNet

We implemented the PaletteNet model with PyTorch based on [this implementation](https://github.com/AakritiKinra/PaletteNet-Implementation).
Inside that repository you could find the paper, in case you'd like to develop and train your model.

There is a lot of room for improvement as the shape of the input is reduced to only 6 colors.

Here are some results that you could compare with other. On our point of view, AI model it seems working great with wallpaper.

**Original**

[![Original](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/test-profile.jpg)](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/test-profile.jpg)

**AI processed - Aurora palette from Nordtheme**

[![Converted](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/test-profile-ai-aurora.jpg)](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/test-profile-ai-aurora.jpg)

-----

**Original**

[![Original](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/sh.png)](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/sh.png)

**AI processed - Nordtheme**

[![Converted](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/test-sh-ai.png)](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/test-sh-ai.png)

-----

**Original**

[![Original](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/valley.jpg)](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/valley.jpg)

**AI processed - Nordtheme**

[![Converted](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/test-valley-ai.jpg)](https://raw.githubusercontent.com/Schrodinger-Hat/ImageGoNord-pip/master/images/test-valley-ai.jpg)

-----

You can also convert videos into the nord palette (or others). Here is an example:  
**Original**  

https://github.com/05Alston/ImageGoNord-pip/assets/89850018/76d4c4a6-9660-4a02-9f46-e5f3f6d0147a

**Processed with algorithm**

https://github.com/05Alston/ImageGoNord-pip/assets/89850018/13822280-c019-49b1-92f7-7c658b33a01d

### Core Technical Concepts

We are using the PIL because it is the most simple library and it is very useful when you need to manipulate some images.

Our goal is also to make this project open source and maintainable by the community. We would love to.

*We believe in the open source community.*

### Getting Started

Getting it from PIP

```
pip install image-go-nord
```

or can be install with extra AI

```
pip install image-go-nord[AI]
```

Then you can use [some example](https://github.com/Schrodinger-Hat/ImageGoNord-pip/tree/master/docs/example) to getting started properly!

### CLI
A CLI Entry point os provide by the installer `image-go-nord`, the file location depend of you setting. Normally it work out of the box the entry point will be into good PATH location.

Actually No manual page is provide , you should use `image-go-nord --help`, to obtain options description.

``` text
usage: image-go-nord [-h] [--avg] [--ai] [--blur] [--quantize] [--base64] [--resize WEIGHT HEIGHT] [--reset-palette] [--add ADD] [-i] [-y] SOURCE [SOURCE ...] TARGET

A tool to convert any RGB image or video to any theme or color palette input by the user. By default the algorithm is pixel-by-pixel and will be disable by --avg or --ai usage.

positional arguments:
  SOURCE                a pathname of an existing file or directory, note: you can chain source like SOURCE [SOURCE ...] in that case TARGET will be consider as directory.
  TARGET                a pathname of an existing or nonexistent file or directory, note: if nonexistent TARGET finish by '/' or '\' it will be consider as directory and will be create if necessary. (no
                        panik if the directory all ready exist it will be use as expected, in that case '/' or '\' is optional).

options:
  -h, --help            show this help message and exit
  --avg                 enable avg algorithm and less colors, if not enable the default is pixel-by-pixel approach, note: that option is disable by --ai usage.
  --ai                  process image by using a PyTorch model 'PaletteNet' for recoloring the image, note: that disable pixel-by-pixel and avg algorithms.
  --blur                enable blur
  --quantize            enable quantization digital image processing, it reduces the number of distinct colors in an image while maintaining its overall visual quality.
  --base64              enable base64 convertion during processing phase.
  --resize WEIGHT HEIGHT
                        resize the image during pre-processing phase.
  --reset-palette       reset the palette to zero color, you can add colors with multiple --add ADD calls.
  --add ADD             add color by hex16 code '#FF0000', name: 'AURORA', 'FROST', 'POLAR_NIGHT', 'SNOW_STORM' or an existing file path it contain a color palette, one hex base 16 peer line ex: #FFFFFF
                        . note: --add ADD can be call more of one time, no trouble to mixe them.
  -i, --interactive     write a prompt for confirmation about: start processing, overwrite a existing file, by default no questions is asking. note: during prompt if response is 'N', a filename will be
                        found automatically.
  -y, --yes             automatically by pass question by confirm with 'Y', that mean yes to continue and yes to overwrite existing files, note: by default prompt questions.
```

##### Important to know

You should care about `-y` and `--yes` option, by use it option you accept in advance to reply Yes to each future questions, 
it can be apply to overwrite file. By default it option is disable.

An other important argument is `-i` and `--interactive`, by default it have no interaction with the user, the commande 
can be use inside a SHELL script, If use interactive `image-go-nord` CLI will asking for confirmation for overwrite a file, 
or before the processing start.

Alls SOURCE, TARGET or ADD have strong capability, look user friendly, read the --help and exemple section

The tool have 3 modes **pixel-by-pixel**, **avg** and **ai**
##### image-go-nor CLI Philosophy
The power is let to the end user

`image-go-nord` CLI have been code as a power tool, we can measure the strong of a tool by it capacity to break everything. 
The tool respect what the user asking for and do not try to mitigate any user mistake.

That is defencive code, all controls are doing at the entrance of datas, it have no control during processing.
If arguments are not correct `image-go-nord` will inform the user by a short message, and have no capability to 
start processing.

#### CLI Examples
##### Pixel by Pixel
That the first command line to try, 
``` shell
image-go-nord image.jpg image-converted.jpg
```
Where `image.jpg` is the image you want convert (SOURCE) and `image-converted.jpg` the final result image (TARGET)

You can use a directory as TARGET , `image-go-nord` will search automatically a filename by try to increase copy file number
``` shell
image-go-nord image.jpg ./
```
In that case TARGET will be define automatically to `image-1.jpg`

``` shell
image-go-nord image.jpg ./
```
##### AVG
`--avg` option disable the pixel-by-pixel mode
``` shell
image-go-nord --avg image.jpg ./
```

##### AI
`--ai` option disable both pixel-by-pixel and avg modes
``` shell
image-go-nord --ai image.jpg ./
```
##### Hack of the day
``` shell
image-go-nord --ai --resize 1920 1080 ./images/ ./unexistent_directory
image-go-nord --avg --reset-palette --add ./palette.txt ./images/ ./
image-go-nord --avg --blur --quantize ./images/ ./
image-go-nord --avg --quantize --interactive ./images/ ./
image-go-nord --avg --quantize --yes ./images/ ./
image-go-nord --reset-palette --add "#000000" --add "#FFFFFF" --add "#777777" --interactive ./images/ ./
image-go-nord image1.jpg image2.png ./image_directory1 ./image_directory2 ./destination/unexistant
```

## Contributing
- Follow the contributor guidelines
- Follow the code style / requirements
- Format for commit messages

# Authors

* [TheJoin95](https://github.com/TheJoin95)
* [Wabri](https://github.com/Wabri)
* [Hierosme](https://github.com/hierosme) - `image-go-nord` CLI

### License

[AGPLv3 license](https://github.com/Schrodinger-Hat/ImageGoNord-pip/blob/master/LICENSE)
