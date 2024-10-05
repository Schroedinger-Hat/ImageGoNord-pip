import pathlib
from setuptools import setup, find_packages

ROOT = pathlib.Path('.')
README = (ROOT / "README.md").read_text()

setup(
    name="image-go-nord",
    version="1.2.0",
    description="A tool to convert any RGB image or video to any theme or color palette input by the user",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Schrodinger-Hat/ImageGoNord-pip",
    download_url = 'https://github.com/Schrodinger-Hat/ImageGoNord-pip/releases',
    keywords = ['nordtheme', 'pillow', 'image', 'conversion', 'rgb', 'color-scheme', 'color-palette', 'linux-rice', 'gruvbox', 'catpuccin'], 
    author="Schrodinger Hat",
    author_email="schrodinger.hat.show@gmail.com",
    license="AGPL-3.0",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    project_urls={
        "Homepage": "https://ign.schrodinger-hat.it",
        "Source": "https://github.com/Schrodinger-Hat/ImageGoNord-pip",
        "Bug Reports": "https://github.com/Schrodinger-Hat/ImageGoNord-pip/issues",
    },
    packages=find_packages(),
    package_data={'': ['*.txt', 'palettes/*.txt']},
    include_package_data=True,
    install_requires=["Pillow", "ffmpeg-python", "numpy", "requests"],
    extras_require = {
        'AI':  ["torch", "scikit-image", "torchvision"]
    },
    python_requires=">=3.5"
)
