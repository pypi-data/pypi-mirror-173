from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Support programming with Kiwrious sensor'
LONG_DESCRIPTION = 'A package that build connection with and provide help for programming with Kiwrious sensors'

# Setting up
setup(
    name="pyKiwrious",
    version=VERSION,
    author="Team 36",
    author_email="hussel@ahlab.org",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyserial', 'numpy', 'unittest'],
    keywords=['python', 'sensor'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)