# ImicusFAT

An Improved FAT/PAP System for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth).

ImicusFAT will work alongside the built-in AA-FAT System and bFAT (on which this app is based on). Data does not share, however you can migrate their data to ImicusFAT, more information below.

## Contents

- [Installation](#installation)
- [Updating](#updating)
- [Data Migration from AA-FAT](#data-migration-from-aa-fat)
- [Credits](#credits)

## Installation

**Important**: This app is a plugin for Alliance Auth. If you don't have Alliance Auth running already, please install it first before proceeding. (see the official [AA installation guide](https://allianceauth.readthedocs.io/en/latest/installation/allianceauth.html) for details)

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

## Data Migration from AA-FAT

Right after the initial installation and running migrations, you can import the data from Alliance Auth's own FAT system if you have used it until now.

**!!Important!!**

Only do this once and only before you are using ImicusFAT.

### Import

To import your old FAT data from Alliance Auth's own FAT you have to disable foreign key checks temporarily.


```
INSERT INTO imicusfat_ifat (id, `system`, shiptype, character_id, ifatlink_id)
SELECT id,`system`,shiptype,character_id,fatlink_id
FROM fleetactivitytracking_fat;

INSERT INTO imicusfat_ifatlink (id, ifattime, fleet, hash, creator_id)
SELECT id,fatdatetime,fleet,hash,creator_id 
FROM fleetactivitytracking_fatlink;
```

## Credits
• ImicusFAT • Developed and Maintained by @exiom with @Aproia and @ppfeufer • Based on [allianceauth-bfat](https://gitlab.com/colcrunch/allianceauth-bfat) by @colcrunch •
