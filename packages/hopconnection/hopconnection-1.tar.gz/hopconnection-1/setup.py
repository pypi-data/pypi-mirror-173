from setuptools import setup, find_packages
import codecs
import os

VERSION = '1'
DESCRIPTION = 'hop connection test pkg'

# Setting up
setup(
    name="hopconnection",
    version=VERSION,
    author="hop",
    author_email="<peacfulsoul18@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning"
    ]
)