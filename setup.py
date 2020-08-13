# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from imicusfat import __version__

install_requires = [
    'django-bootstrap-form',
    'allianceauth>=2.0',
]

testing_extras = [

]

setup(
    name='allianceauth-imicusfat',
    version=__version__,
    author='Aproia Raholan',
    author_email='evictus.iou@gmail.com',
    description='Alliance Auth FAT/PAP System for Evictus',
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
        ':python_version=="3.4"': ['typing'],
    },
    python_requires='~=3.4',
    license='GPLv3',
    packages=find_packages(),
    url='https://gitlab.com/evictus.iou/allianceauth-imicusfat',
    zip_safe=False,
    include_package_data=True,
)