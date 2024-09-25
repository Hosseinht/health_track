from django.db.models.signals import post_delete
from django.dispatch import receiver

from patients.models import Patient


@receiver(post_delete, sender=Patient)
def delete_address(sender, instance, **kwargs):
    if instance.address:
        instance.address.delete()
