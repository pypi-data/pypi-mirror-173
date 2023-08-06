from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.1'
DESCRIPTION = 'Shamir\'s Secret Sharing Encoder'
LONG_DESCRIPTION = 'Shamir\'s Secret Sharing Encoder for educational purposes.'

# Setting up
setup(
    name="ShamirEncoder",
    version=VERSION,
    author="PunGrumpy",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'shamir', 'education', 'encoder'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
