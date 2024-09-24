from datetime import date

from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class Address(models.Model):
    address_one = models.CharField(max_length=400)
    address_two = models.CharField(max_length=400)
    country = CountryField(null=True, blank=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=30, blank=True, null=True)


class Patients(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.OneToOneField(
        Address, on_delete=models.SET_NULL, null=True, related_name="patient"
    )
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        default=Gender.OTHER,
    )
    phone_number = PhoneNumberField(max_length=30)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )
