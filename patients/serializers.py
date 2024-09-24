from rest_framework import serializers

from patients.models import Patient


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
