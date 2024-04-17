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

Then you can use [some example](https://github.com/Schrodinger-Hat/ImageGoNord-pip/tree/master/docs/example) to getting started properly!

### Contributing
- Follow the contributor guidelines
- Follow the code style / requirements
- Format for commit messages

# Authors

[TheJoin95](https://github.com/TheJoin95) & [Wabri](https://github.com/Wabri)

### License

[AGPLv3 license](https://github.com/Schrodinger-Hat/ImageGoNord-pip/blob/master/LICENSE)
