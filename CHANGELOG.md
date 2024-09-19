# Changelog
All notable changes to this project will be documented in this file.
## 1.1.1 - 19 sept 2024
* Migrate to pyproject.toml module format
  * Keep setuptools version inside setup.py, and permit to be overwritten by APPLICATION_VERSION environment variable
  * Define submodule one by one `models`, `palettes` and `utility`
  * 
* ``image-go-nord`` CLI entry point
  * Define a consistent ``argpare`` parser
  * Define a class `ImageGoNordCLI` dedicated to the entry point
  * Exit code management
  * Define property getter/setter for `target`, `source` and `size`, where the logic is apply
  * Force argparse to use they properties
  * Add support for use files or directories as `target` and `source`
  * Add support for `--add` it support colors, palette file, color name
  * Add support for AVG `--add`
  * Add support for AI `--ai` it use coloration over AI
  * Add support for quantize `--quantize`
  * Add support for `--resize` it permit to force size during the pre-processing
* Update README.md for introduce image-go-nord CLI
* Migrate pytest to pyproject.toml module format
  * Add ``image-go-nord`` CLI test file
