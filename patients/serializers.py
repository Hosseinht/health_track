from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from patients.models import Address, Patient


class AddressSerializer(serializers.ModelSerializer):
    country = CountryField()

    class Meta:
        model = Address
        fields = [
            "address_one",
            "address_two",
            "country",
            "city",
            "postal_code",
        ]


class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "first_name",
            "last_name",
            "gender",
            "phone_number",
            "date_of_birth",
            "age",
        ]


class PatientCreateSerializer(serializers.ModelSerializer):
    clinician = serializers.HiddenField(default=serializers.CurrentUserDefault())
    address = AddressSerializer()

    class Meta:
        model = Patient
        fields = [
            "clinician",
            "first_name",
            "last_name",
            "address",
            "gender",
            "phone_number",
            "date_of_birth",
        ]


class PatientDetailSerializer(serializers.ModelSerializer):
    clinician = serializers.ReadOnlyField(source="clinician.email")
    address = AddressSerializer()

    class Meta:
        model = Patient
        fields = [
            "id",
            "clinician",
            "first_name",
            "last_name",
            "address",
            "gender",
            "phone_number",
            "date_of_birth",
            "full_name",
            "age",
        ]


class PatientUpdateSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Patient
        fields = [
            "first_name",
            "last_name",
            "address",
            "gender",
            "phone_number",
            "date_of_birth",
        ]
