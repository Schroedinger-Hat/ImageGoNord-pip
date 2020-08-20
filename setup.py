import pathlib
from setuptools import setup, find_packages

ROOT = pathlib.Path('.')
README = (ROOT / "README.md").read_text()

setup(
    name="image-go-nord",
    version="0.0.8",
    description="A tool for converting RGB image to Nordtheme palette",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Schrodinger-Hat/ImageGoNord-pip",
    download_url = 'https://github.com/Schrodinger-Hat/ImageGoNord-pip/releases',
    keywords = ['nordtheme', 'pillow', 'image', 'conversion', 'rgb', 'color-scheme', 'color-palette'], 
    author="Schrodinger Hat",
    author_email="schrodinger.hat.show@gmail.com",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    project_urls={
        "Homepage": "https://ign.schrodinger-hat.it",
        "Source": "https://github.com/Schrodinger-Hat/ImageGoNord-pip",
        "Bug Reports": "https://github.com/Schrodinger-Hat/ImageGoNord-pip/issues",
    },
    packages=find_packages(),
    package_data={'ImageGoNord': ['palettes/*.txt']},
    include_package_data=True,
    install_requires=["Pillow"],
    python_requires=">=3.5"
)
