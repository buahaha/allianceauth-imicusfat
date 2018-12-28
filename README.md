# allianceauth-bfat

A better FAT system for Alliance Auth.

## Installation

**IMPORTANT NOTE**: This is a _replacement_ for `allianceauth.fleetactivitytracking` and **cannot** be installed alongside it. If you are currently using the FAT system that ships with AA. You will want to back up your database, and uninstall it. (Remember to do `python manage.py migrate fleetactivitytracking zero` before removing it from `INSTALLED_APPS`!)

`pip install git+https://gitlab.com/colcrunch/allianceauth-bfat.git`

Add to your `INSTALLED_APPS`
```py
'bfat',
```

If you are using mysql, you need to add the timezone tables to your database. For instructions, please see this link: https://dev.mysql.com/doc/refman/5.5/en/mysql-tzinfo-to-sql.html Users using sqlite do not need to worry about this.

Restart your workers.


## Alliance Auth Settings (local.py)
Paps vs. Fats... which do you prefer?

Add the following line to your local.py settings if you would like to use PAP instead of FAT.
```py
FAT_AS_PAP = True
```
