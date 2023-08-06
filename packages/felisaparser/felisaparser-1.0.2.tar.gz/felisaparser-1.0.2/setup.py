from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = 'felisaparser',
    version = '1.0.2',
    description = 'This package contains a function to directly parse a excel file into a csv file',
    author = 'Adrián Martínez, David Del Río',
    url = 'https://github.com/daviddelriod/felisaparser',
    keywords = 'xlsx parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires = [
        'pandas',
        ],
)