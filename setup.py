from os.path import dirname
from os.path import join
import re

from setuptools import setup


def read(*path):
    with open(
            join(dirname(__file__), *path),
            encoding="utf8"
    ) as fp:
        return fp.read()


def find_version(*path):
    version_file = read(*path)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="rucola",
    version=find_version('rucola.py'),
    license="MIT",

    description="A simple framework (not only) for static sites generation",
    long_description=read("README.rst") + '\n\n' + read("CHANGES"),

    author="Kasper Minciel",
    author_email="kasper.minciel@gmail.com",

    url="https://github.com/lecnim/rucola",

    py_modules=['rucola'],
    include_package_data=True,
    zip_safe=False,

    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities"
    ],

    # pip instalucolal rucola[plugins]
    extras_require={
        'plugins': ['rucola-ignore',
                    'rucola-markdown',
                    'rucola-mustache',
                    'rucola-yamlfm']
    }

)
