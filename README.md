# ImicusFAT

[![pipeline status](https://gitlab.com/evictus.iou/allianceauth-imicusfat/badges/master/pipeline.svg)](https://gitlab.com/evictus.iou/allianceauth-imicusfat/commits/master)
[![version](https://img.shields.io/pypi/v/allianceauth-imicusfat?label=release)](https://pypi.org/project/allianceauth-imicusfat/)
[![license](https://img.shields.io/badge/license-GPLv3-green)](https://pypi.org/project/allianceauth-imicusfat/)
[![python](https://img.shields.io/pypi/pyversions/allianceauth-imicusfat)](https://pypi.org/project/allianceauth-imicusfat/)
[![django](https://img.shields.io/pypi/djversions/allianceauth-imicusfat?label=django)](https://pypi.org/project/allianceauth-imicusfat/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](http://black.readthedocs.io/en/latest/)

An Improved FAT/PAP System for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth). 

### Feature Highlights/Differences
- FATLink Creation and Population from ESI
- Fleet Type Classification (can be added in the Admin Menu)
- Graphical Statistics Views
- Many Core Functionality Improvements and Fixes

ImicusFAT will work alongside the built-in AA-FAT System and bFAT*. However data does not share, but you can migrate their data to ImicusFAT, for more information see below.

## Contents

- [Installation](#installation)
- [Updating](#updating)
- [Data Migration](#data-migration)
    - [Import from AA-FAT](#import-from-aa-fat)
    - [Import from bFAT](#import-from-bfat)
- [Credits](#credits)

## Installation

**Important**: This app is a plugin for Alliance Auth. If you don't have Alliance Auth running already, please install it first before proceeding. (see the official [AA installation guide](https://allianceauth.readthedocs.io/en/latest/installation/allianceauth.html) for details)
**Important**: For users migrating from bFAT, please read [Migrating from bFAT](#migrating-from-bfat) specific instructions FIRST.

### Step 1 - Install app

Make sure you are in the virtual environment (venv) of your Alliance Auth installation. Then install the latest version:

```bash
pip install allianceauth-imicusfat
```

### Step 2 - Update your AA settings

Configure your AA settings (`local.py`) as follows:

- Add `'imicusfat',` to `INSTALLED_APPS`

### Step 3 - Finalize the installation

Run migrations & copy static files

```bash
python manage.py collectstatic
python manage.py migrate
```

Restart your supervisor services for AA.

## Updating

To update your existing installation of ImicusFAT, first enable your virtual environment (venv) of your Alliance Auth installation.

```bash
pip install -U allianceauth-imicusfat

python manage.py collectstatic
python manage.py migrate
```

Finally restart your supervisor services for AA

## Data Migration

Right after the initial installation and running migrations, you can import the data from Alliance Auth's own FAT system or bFAT, if you have used it until now.

**!!IMPORTANT!!**

Only do this once and ONLY BEFORE you are using ImicusFAT.

### Import from AA-FAT

```bash
python myauth/manage.py imicusfat_import_from_allianceauth_fat
```

### Import from bFAT

```bash
python myauth/manage.py imicusfat_import_from_bfat
```

## Credits
• ImicusFAT • Developed and Maintained by @exiom with @Aproia and @ppfeufer • Based on [allianceauth-bfat](https://gitlab.com/colcrunch/allianceauth-bfat) by @colcrunch •
