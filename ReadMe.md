# ImicusFAT

An Improved FAT/PAP System for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth).<br>
ImicusFAT will work alongside the built-in AA FAT System and bFAT. <br>
Data does not share, however you can migrate their data to ImicusFAT, more information below.


## Installation

`pip install git+https://gitlab.com/evictus.iou/allianceauth-imicusfat.git`

Add to your `INSTALLED_APPS`
```py
'imicusfat',
```

Run migrations and collect static files

```python
python manage.py collectstatic
python manage.py migrate
```

#### Data Migration from AA-FAT
```
Disable foreign key checks

INSERT INTO imicusfat_ifat (id, `system`, shiptype, character_id, ifatlink_id)
SELECT id,`system`,shiptype,character_id,fatlink_id
FROM fleetactivitytracking_fat;

INSERT INTO imicusfat_ifatlink (id, ifattime, fleet, hash, creator_id)
SELECT id,fatdatetime,fleet,hash,creator_id 
FROM fleetactivitytracking_fatlink;
```


#### Timezone Tables
If you are using mysql, you need to add the timezone tables to your database.<br>
For instructions, please see this link: https://dev.mysql.com/doc/refman/5.5/en/mysql-tzinfo-to-sql.html <br>
Restart Alliance Auth.



## Credits
• ImicusFAT • Developed and Maintained by @exiom with @Aproia and @ppfeufer • Based on [allianceauth-bfat](https://gitlab.com/colcrunch/allianceauth-bfat) by @colcrunch •
