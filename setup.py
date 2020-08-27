# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from imicusfat import __version__


install_requires = [
    "django-bootstrap-form",
    "allianceauth>=2.7.2",
]

testing_extras = []

setup(
    name="allianceauth-imicusfat",
    version=__version__,
    author="Exiom, Aproia, ppfeufer",
    author_email="evictus.iou@gmail.com",
    description="Alliance Auth FAT/PAP System for Evictus",
    install_requires=install_requires,
    extras_require={"testing": testing_extras, ':python_version=="3.6"': ["typing"],},
    python_requires="~=3.6",
    license="GPLv3",
    packages=find_packages(),
    url="https://gitlab.com/evictus.iou/allianceauth-imicusfat",
    zip_safe=False,
    include_package_data=True,
)
