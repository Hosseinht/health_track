from django.contrib import admin

from .models import Address, Assessment, Patient

# Register your models here.
admin.site.register(Address)
admin.site.register(Patient)
admin.site.register(Assessment)
