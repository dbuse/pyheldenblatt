from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyheldenblatt',

    # TODO: enhance versioning
    version='0.1.0rc4',

    description='character sheet generator for the p&p rpg "Das Schwarze Auge"',
    long_description=long_description,

    # TODO: create public project website and add it here
    url='https://dav.toifras.de/hg/pyheldenblatt',

    author='Dominik S. Buse',
    author_email='dbuse@toifras.de',

    # Keep in sync with LICENSE.txt
    license='Apache 2.0',

    # TODO: add classifiers -- audience, topic and version support
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
    ],

    keywords='DSA character sheet generator heldenblatt heldenbogen',

    packages=find_packages(exclude=['data', 'helden']),

    install_requires=['fpdf>=1.7.2'],

    # TODO: add dep groups for developement/testing
    extras_require={},

    # TODO: filter out really required (background) images files
    package_data={'pyheldenblatt': ['data/*.tsv', 'data/font/*.ttf', 'data/img/*.jpg', 'data/img/*.png']},

    # TODO: convert cli script into entry point
    entry_points={},
)
