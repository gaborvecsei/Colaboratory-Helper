from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='colabber',
    version='0.0.1',
    description='Google Colaboratory helper scripts',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gaborvecsei.com',
    author='Gabor Vecsei',
    license='MIT',
    packages=find_packages(),
)
