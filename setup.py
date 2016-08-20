# coding=utf8

from setuptools import setup,find_packages

import os


def read(f):
    open(os.path.join(os.path.dirname(__file__),f)).read().strip()


DESCRIPTION = "tornado_hbredis is an asynchronous redis client for tornado"

setup(
    name="tornado_hbredis",
    version=0.1,
    author="HuangBiao",
    author_email="19941222hb@gmail.com",
    description=DESCRIPTION,
    long_description=read("README.rst"),
    license="MIT",
    url="https://github.com/free-free/tornado_hbredis",
    download_url="https;//github.com/free-free/tornado_hbredis",
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
