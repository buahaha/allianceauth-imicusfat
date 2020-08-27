# ImicusFAT

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
pip install git+https://gitlab.com/evictus.iou/allianceauth-imicusfat.git
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
pip install -U git+https://gitlab.com/evictus.iou/allianceauth-imicusfat.git

python manage.py collectstatic
python manage.py migrate
```

Finally restart your supervisor services for AA

## Data Migration

Right after the initial installation and running migrations, you can import the data from Alliance Auth's own FAT system or bFAT, if you have used it until now.

**!!IMPORTANT!!**

Only do this once and ONLY BEFORE you are using ImicusFAT.

### Import from AA-FAT

To import your old FAT data from Alliance Auth's own FAT, you have to disable foreign key checks temporarily.


```
INSERT INTO imicusfat_ifat (id, `system`, shiptype, character_id, ifatlink_id)
SELECT id,`system`,shiptype,character_id,fatlink_id
FROM fleetactivitytracking_fat;

INSERT INTO imicusfat_ifatlink (id, ifattime, fleet, `hash`, creator_id)
SELECT id,fatdatetime,fleet,hash,creator_id 
FROM fleetactivitytracking_fatlink;
```

### Migrating from bFAT

Before installation, temporarily comment out `bfat` in your AA settings (`local.py`) by doing:

- Modify `'bfat',` to `#'bfat',` under `INSTALLED_APPS`

And then continue installation as normal. You may undo this after successful installation.

#### Import from bFAT
To import your old FAT data from bFAT, you have to disable foreign key checks temporarily.


```
INSERT INTO imicusfat_clickifatduration (id, duration, fleet_id)
SELECT id, duration, fleet_id
FROM bfat_clickfatduration;

INSERT INTO imicusfat_dellog (id, deltype, string, remover_id)
SELECT id, deltype, string, remover_id
FROM bfat_dellog;

INSERT INTO imicusfat_ifat (id, `system`, shiptype, character_id, ifatlink_id)
SELECT id,`system`,shiptype,character_id,fatlink_id
FROM bfat_fat;

INSERT INTO imicusfat_ifatlink (id, ifattime, fleet, `hash`, creator_id)
SELECT id,fattime,fleet,hash,creator_id 
FROM bfat_fatlink;

INSERT INTO imicusfat_manualifat (id, character_id, creator_id, ifatlink_id)
SELECT id, character_id, creator_id, fatlink_id
FROM bfat_manualfat;
```

## Credits
• ImicusFAT • Developed and Maintained by @exiom with @Aproia and @ppfeufer • Based on [allianceauth-bfat](https://gitlab.com/colcrunch/allianceauth-bfat) by @colcrunch •
