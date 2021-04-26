from ImageGoNord import NordPaletteFile, GoNord

go_nord = GoNord()
"""image = go_nord.open_image("images/test-profile.jpg")
go_nord.convert_image(image, save_path='images/test.processed.jpg') """

# E.g. Avg algorithm and less colors
go_nord.enable_avg_algorithm()
# go_nord.reset_palette()
# go_nord.set_palette_lookup_path('./mypalette')
# go_nord.add_file_to_palette(NordPaletteFile.POLAR_NIGHT)
# go_nord.add_file_to_palette(NordPaletteFile.SNOW_STORM)
# go_nord.add_color_to_palette('#FF0000')
# go_nord.set_default_nord_palette()

image = go_nord.open_image("images/bn.jpg")
go_nord.convert_image(image, save_path='images/test.avg.jpg')

# E.g. Resized img no Avg algorithm and less colors
go_nord.disable_avg_algorithm()
go_nord.reset_palette()
go_nord.add_file_to_palette(NordPaletteFile.POLAR_NIGHT)
go_nord.add_file_to_palette(NordPaletteFile.SNOW_STORM)

image = go_nord.open_image("images/test.jpg")
resized_img = go_nord.resize_image(image)
go_nord.convert_image(resized_img, save_path='images/test.resized.jpg')

# E.g. Quantize

image = go_nord.open_image("images/test.jpg")
go_nord.reset_palette()
go_nord.set_default_nord_palette()
quantize_image = go_nord.quantize_image(image, save_path='images/test.quantize.jpg')

# To base64
go_nord.image_to_base64(quantize_image, 'jpeg')
