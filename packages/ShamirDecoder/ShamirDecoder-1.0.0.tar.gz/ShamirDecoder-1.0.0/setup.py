from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.0'
DESCRIPTION = 'Shamir\'s Secret Sharing Decoder'
LONG_DESCRIPTION = 'Shamir\'s Secret Sharing Decoder for educational purposes.'

# Setting up
setup(
    name="ShamirDecoder",
    version=VERSION,
    author="PunGrumpy",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'shamir', 'education', 'decoder'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
