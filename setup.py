# coding=utf8

from setuptools import setup,find_packages
import re
import os 

def read(f):
    return open(os.path.join(os.path.dirname(__file__),f)).read().strip()

def find_version(f):
    file_content = read(f)
    try:
        return re.findall(r'__version__ = "([^\'\"]+)"\r?$',
            file_content, re.M)[0]
    except IndexError:
        raise RuntimeError("Can find version number")


DESCRIPTION = "tornado_hbredis is an asynchronous redis client for tornado"

setup(
    name="tornado_hbredis",
    version=find_version("tornado_hbredis/__init__.py"),
    author="HuangBiao",
    author_email="19941222hb@gmail.com",
    description=DESCRIPTION,
    long_description=read("README.rst"),
    license="MIT",
    url="https://github.com/free-free/tornado_hbredis",
    packages=find_packages(),
    install_requires=["tornado","tornadis"],
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)
