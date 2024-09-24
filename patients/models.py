from datetime import date

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class Address(models.Model):
    address_one = models.CharField(max_length=400)
    address_two = models.CharField(max_length=400)
    country = CountryField(null=True, blank=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=30, blank=True, null=True)


class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    clinician = models.ForeignKey(User, on_delete=models.CASCADE)
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


class Assessment(models.Model):
    class TYPES(models.TextChoices):
        COGNITIVE = (
            "cognitive",
            "Cognitive Status",
        )
        PHYSICAL = (
            "physical",
            "Physical Ability",
        )
        MENTAL = (
            "mental",
            "Mental Health",
        )
        SOCIAL = (
            "emotional",
            "Emotional Well-being",
        )

    clinician = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    assessment_type = models.CharField(max_length=50, choices=TYPES)
    assessment_data = models.DateTimeField(default=timezone.now())
    final_score = models.SmallIntegerField()

    def __str__(self):
        return f"{self.patient} - {self.assessment_type}"
