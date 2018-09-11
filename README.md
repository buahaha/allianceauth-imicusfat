# allianceauth-bfat

A better FAT system for Alliance Auth.

## Installation
`pip install git+https://gitlab.com/colcrunch/allianceauth-bfat.git`

Add to your `INSTALLED_APPS`
```py
'bfat',
```

Restart your workers.


## Alliance Auth Settings (local.py)
Paps vs. Fats... which do you prefer?

Add the following line to your local.py settings if you would like to use PAP instead of FAT.
```py
FAT_AS_PAP = True
```
