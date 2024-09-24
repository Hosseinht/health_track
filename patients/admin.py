from django.contrib import admin

from .models import Address, Patient

# Register your models here.
admin.site.register(Address)
admin.site.register(Patient)
