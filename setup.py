# coding=utf8

from setuptools import setup,find_packages

DESCRIPTION = "tornado_hbredis is an async redis client for tornado,it'a actually encapsulation fro tornadis"

setup(
    name="tornado_hbredis",
    version="0.0.1",
    author="HUANGBIAO",
    author_email="19941222hb@gmail.com",
    url="https://github.com/free-free/tornado_hbredis",
    packages=find_packages(),
    LICENSE="MIT",
    download_url="https;//github.com/free-free/tornado_hbredis",
    description=DESCRIPTION,
    install_requires=["tornado","tornadis"]
)
