from django.contrib import admin

from .models import Address, Patients

# Register your models here.
admin.site.register(Address)
admin.site.register(Patients)
