from ImageGoNord import NordPaletteFile, GoNord

go_nord = GoNord()
palettedata = go_nord.get_palette_data()
image = go_nord.open_image("images/test.jpg")
go_nord.convert_image(image, palettedata, save_path='images/test.processed.jpg')


# E.g. Avg algorithm and less colors
go_nord.enable_avg_algorithm()
go_nord.reset_palette()
go_nord.add_file_to_palette(NordPaletteFile.POLAR_NIGHT)
go_nord.add_file_to_palette(NordPaletteFile.SNOW_STORM)

palettedata = go_nord.get_palette_data()
image = go_nord.open_image("images/test.jpg")
go_nord.convert_image(image, palettedata, save_path='images/test.avg.jpg')

# E.g. Resized img no Avg algorithm and less colors
go_nord.disable_avg_algorithm()
go_nord.reset_palette()
go_nord.add_file_to_palette(NordPaletteFile.POLAR_NIGHT)
go_nord.add_file_to_palette(NordPaletteFile.SNOW_STORM)

palettedata = go_nord.get_palette_data()
image = go_nord.open_image("images/test.jpg")
resized_img = go_nord.resize_image(image)
go_nord.convert_image(resized_img, palettedata, save_path='images/test.resized.jpg')

# E.g. Quantize

palettedata = go_nord.get_palette_data()
image = go_nord.open_image("images/test.jpg")
quantize_image = go_nord.quantize_image(image)
# go_nord.image_to_base64(image, 'jpeg')
