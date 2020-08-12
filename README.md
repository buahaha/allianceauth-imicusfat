# allianceauth-imicusfat

A FAT system built for the Evictus Alliance. Allows for usage alongside built in FAT system.



If you are using mysql, you need to add the timezone tables to your database. For instructions, please see this link: https://dev.mysql.com/doc/refman/5.5/en/mysql-tzinfo-to-sql.html Users using sqlite do not need to worry about this.

Restart your workers.


## Alliance Auth Settings (local.py)
Paps vs. Fats... which do you prefer?

Add the following line to your local.py settings if you would like to use PAP instead of FAT.
```py
FAT_AS_PAP = True
```
