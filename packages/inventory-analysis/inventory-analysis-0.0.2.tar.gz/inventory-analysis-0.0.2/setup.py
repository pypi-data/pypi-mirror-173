from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'

# Setting up
setup(
    name="inventory-analysis",
    version=VERSION,
    author="Ivan Vallenas",
    author_email="<ivan.vallenas.munoz@gmail.com>",
    url="https://github.com/ivanvallenas/inventory-analysis",
    description="Inventory Analysis package",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['opencv-python', 'pyautogui', 'pyaudio'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)