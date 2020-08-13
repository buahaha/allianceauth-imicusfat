# ImicusFAT

FAT/PAP System for Alliance Auth. Built for the Evictus Alliance. 


## Installation

ImicusFAT will work alongside the built-in AA FAT System.

`pip install git+https://gitlab.com/evictus.iou/allianceauth-imicusfat.git`

Add to your `INSTALLED_APPS`
```py
'imicusfat',
```

#### Timezone Tables
If you are using mysql, you need to add the timezone tables to your database.<br>
For instructions, please see this link: https://dev.mysql.com/doc/refman/5.5/en/mysql-tzinfo-to-sql.html <br>
Restart Alliance Auth.


## Alliance Auth Settings (local.py)
#### PAPs vs. FATs... which do you prefer?
Add the following line to your local.py settings if you would like to use PAP instead of FAT.
```py
FAT_AS_PAP = True
```

## Credits
• ImicusFAT • Developed and Maintained by @Aproia with @exiom • Based on [allianceauth-bfat](https://gitlab.com/colcrunch/allianceauth-bfat) by @colcrunch •