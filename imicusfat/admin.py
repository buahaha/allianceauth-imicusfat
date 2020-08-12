from django.contrib import admin

from .models import Fat, FatLink

# Register your models here.
admin.site.register(FatLink)
admin.site.register(Fat)
