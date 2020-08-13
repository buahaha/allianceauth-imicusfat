# allianceauth-imicusfat

FAT/PAP System for Alliance Auth. Built for the Evictus Alliance. 


## Installation

imicusfat will alongside the built-in AA FAT System.

`pip install git+https://gitlab.com/evictus.iou/allianceauth-imicusfat.git`

Add to your `INSTALLED_APPS`
```py
'imicusfat',
```

If you are using mysql, you need to add the timezone tables to your database. For instructions, please see this link: https://dev.mysql.com/doc/refman/5.5/en/mysql-tzinfo-to-sql.html Users using sqlite do not need to worry about this.

Restart your workers.


## Alliance Auth Settings (local.py)
PAPs vs. FATs... which do you prefer?

Add the following line to your local.py settings if you would like to use PAP instead of FAT.
```py
FAT_AS_PAP = True
```

## Credits
imicusfat is developed and maintained by @Aproia with @exiom, derived from [allianceauth-bfat](https://gitlab.com/colcrunch/allianceauth-bfat) by @colcrunch