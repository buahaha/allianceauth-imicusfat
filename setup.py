# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from bfat import __version__

install_requires = [
    'django-bootstrap-form',
    'allianceauth>=2.0',
]

testing_extras = [

]

setup(
    name='allianceauth-bfat',
    version=__version__,
    author='Col Crunch',
    author_email='it-team@serin.space',
    description='A better FAT system for Alliance Auth',
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
        ':python_version=="3.4"': ['typing'],
    },
    python_requires='~=3.4',
    license='GPLv3',
    packages=find_packages(),
    url='https://gitlab.com/colcrunch/allianceauth-bfat',
    zip_safe=False,
    include_package_data=True,
)
