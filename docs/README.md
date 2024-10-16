
# Documentation

The documentation is under development (as the package) and it is [available also on the website](https://ign.schroedinger-hat.org/documentation/python).
You can find some usage and some example under the example folder.

# Class & Methods

## NordPaletteFile:

A class used to map the nord color-scheme into files.  Each file contains the hex code of the nord palette, divided into:
  - AURORA.txt: Aurora color-palette
  - FROST.txt: Frost color-palette
  - POLAR_NIGHT.txt: Polar night color-palette
  - SNOW_STORM.txt: Snow Storm color-palette

## GoNord

A class used for converting image to the nord palette. It can be used also for converting image to other palette by loading different palette or hex color.
This class needs Pillow and apply 3 different palette conversion algorithm:
  - replace pixel by avg area pixel (convert method)
  - replace pixel by pixel (convert method)
  - apply a filter by using pillow features (quantize method)


### GoNord Attributes

**PALETTE_LOOKUP_PATH**: str - path to look for finding the palette files (.txt)

**USE_GAUSSIAN_BLUR**: bool - enable or disable the blur (in output)

**USE_AVG_COLOR**: bool - enable or disable avg algorithm

**AVG_BOX_DATA**: dict - params (width and height) of the avg area to be considered

**AVAILABLE_PALETTE**: list - loaded palette list

**PALETTE_DATA**: dict - available palette data in hex : rgb format



## Methods

### set_palette_lookup_path
Set the base_path for the palette folder, if different from the default.

`set_palette_lookup_path(self, path)`

-----


### set_default_nord_palette
Set available palette as the default palette.

The default palette is the full Nordtheme palette.

`set_default_nord_palette(self)`

-----


### get_palette_data
Build the palette data from configuration

`get_palette_data(self)`

**Returns**: dict - The palette data: keys are hex color code, values are rgb values

-----


### add_color_to_palette
Add hex color to current palette

`add_color_to_palette(self, hex_color)`

-----


### reset_palette
Reset the available_palette prop

`reset_palette(self)`

-----


### add_file_to_palette
Append a custom file to the available palette

`add_file_to_palette(self, file)`

-----


### enable_gaussian_blur
Enable blur filter
  
`enable_gaussian_blur(self)`

-----


### disable_gaussian_blur
disabled blur filter
  
`disable_gaussian_blur(self)`

-----


### open_image
Load an image using Pillow utility
  
`open_image(self, path)`

**Parameters**:
  - path: str - the path and the filename where to save the image

**Returns**: pillow Image - the opened image

-----


### resize_image
Resize an image using Pillow utility
  
`resize_image(self, image, w=0, h=0)`

**Parameters**
- image: pillow image - The source pillow image
- w: int - New width
- h: int - New height

**Returns**: pillow image - the resized image

-----


### image_to_base64
Convert a Pillow image to base64 string

Available extension: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html

`image_to_base64(self, image, extension)`

**Parameters**
- image: pillow image - The source pillow image
- extension: str - The extension of the source image (mandatory)

**Returns**: pillow image - processed image

-----

### base64_to_image
Convert a base64 string to a Pillow image
  
`base64_to_image(self, img_b64)`

**Parameters**
img_b64: str - The base64 string representation of the image

**Returns**: pillow image - The converted image from base64

-----

### load_pixel_image
Load the pixel map of a given Pillow image
  
`load_pixel_image(self, opened_image)`

**Parameters**
- image: pillow image - The source pillow image

**Returns**: pillow image - pixel map of the opened image

-----


### enable_avg_algorithm
Enable avg algorithm
  
`enable_avg_algorithm(self)`

-----


### disable_avg_algorithm
  Disabled avg algorithm
  
`disable_avg_algorithm(self)`

-----


### set_avg_box_data
Set the dimension of the AVG area box to use
  
`set_avg_box_data(self, w=-2, h=3)`

**Parameters**

- w: int - Box's width
- h: int - Box's height


-----


### quantize_image
Quantize a Pillow image by applying the available palette
  
`quantize_image(self, image, save_path='')`

**Parameters**
- image: pillow image - The source pillow image
- fill_color: str - Default fill color as foreground
- save_path : str, optional - the path and the filename where to save the image

**Returns**: pillow image - quantized image

-----


### convert_image
Process a Pillow image by replacing pixel or by avg algorithm
  
`convert_image(self, image, palettedata, save_path='')`

**Parameters**

- image : pillow image - The source pillow image
- save_path : str, optional - the path and the filename where to save the image

**Returns**: pillow image - processed image

-----


### save_image_to_file
  Save a Pillow image to file
  
`save_image_to_file(self, image, path)`

**Parameters**
- image: pillow image - The source pillow image
- path: str - the path and the filename where to save the image

-----

## Example

### Import GoNord from ImageGoNord package

from ImageGoNord import NordPaletteFile, GoNord

### Use replace pixel by pixel algorithm

```
go_nord = GoNord()
image = go_nord.open_image("images/test.jpg")
go_nord.convert_image(image, save_path='images/test.processed.jpg')
```

### Use Avg algorithm, clean default palette and add just the POLAR NIGHT and SNOW STORM colors
```
go_nord.enable_avg_algorithm()
go_nord.reset_palette()
go_nord.add_file_to_palette(NordPaletteFile.POLAR_NIGHT)
go_nord.add_file_to_palette(NordPaletteFile.SNOW_STORM)
// You can add color also by their hex code
go_nord.add_color_to_palette('#FF0000')

image = go_nord.open_image("images/test.jpg")
go_nord.convert_image(image, save_path='images/test.avg.jpg')
```

### Resize image and use the replace pixel by pixel algorithm with less colors
```
go_nord.disable_avg_algorithm()
go_nord.reset_palette()
go_nord.add_file_to_palette(NordPaletteFile.POLAR_NIGHT)
go_nord.add_file_to_palette(NordPaletteFile.SNOW_STORM)

image = go_nord.open_image("images/test.jpg")
resized_img = go_nord.resize_image(image)
go_nord.convert_image(resized_img, save_path='images/test.resized.jpg')
```

### Use quantize method for rfiltering an image with the current palette
```
image = go_nord.open_image("images/test.jpg")
go_nord.reset_palette()
go_nord.set_default_nord_palette()
quantize_image = go_nord.quantize_image(image, save_path='images/test.quantize.jpg')
// To base64
go_nord.image_to_base64(quantize_image, 'jpeg')
```
