import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if os.path.exists('README.rst'):
    long_description = read('README.rst')
else:
    long_description = 'https://github.com/sightio/tornado-api-kit'

setup(
    name = "tornado-api-kit",
    version = "0.0.1",
    author = "Alexander Tereshkin",
    author_email = "atereshkin@y-node.com",
    description = "A collection of routines for building web APIs on top of Tornado web server. ",
    license = "BSD",
    keywords = "tornado api",
    url = "https://github.com/sightio/tornado-api-kit",
    packages=['apikit'],
    long_description=long_description,
    install_requires=('tornado', 'dict2xml'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",        
    ],
    include_package_data=True,
    entry_points={
    },

)
