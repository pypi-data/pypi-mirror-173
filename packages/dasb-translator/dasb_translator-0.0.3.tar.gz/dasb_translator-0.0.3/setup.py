#!/usr/bin/python
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
    name="dasb_translator",
    version="0.0.3",
    author="Hompeaz",
    author_email="hompeaz@gmail.com",
    description="A CLI translation tool by reading the clipboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Acoustical/Dasb_Translator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "requests",
        "pyperclip",
        "deepl-cli"
    ],
    entry_points={
        'console_scripts': [
            'dasb_translator = dasb_translator:main',
        ],
    }
)
