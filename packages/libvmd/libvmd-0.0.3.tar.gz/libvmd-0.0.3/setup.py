# -*- coding: utf-8 -*-

import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()


    
setuptools.setup(
    name="libvmd",
    version="0.0.3",
    author="Hyoseob Noh",
    author_email="hyoddubi@naver.com",
    description="LIBVMD: Python library for variational mode decomposition for both 1D and 2D",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hyoddubi1/libvmd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'numpy>=1.20.0'
    ]
)