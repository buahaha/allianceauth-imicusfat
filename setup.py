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
    author='Aproia',
    author_email='sogetsu90@gmail.com',
    description='FAT system built from Better FAT system, customised for Evictus',
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
        ':python_version=="3.4"': ['typing'],
    },
    python_requires='~=3.4',
    license='GPLv3',
    packages=find_packages(),
    url='https://gitlab.com/Aproia/allianceauth-bfat',
    zip_safe=False,
    include_package_data=True,
)
