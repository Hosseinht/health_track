from rest_framework import serializers

from patients.models import Address, Assessment, Patient


class AddressSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = [
            "address_one",
            "address_two",
            "country",
            "city",
            "postal_code",
        ]

    def get_country(self, obj):
        return obj.country.name


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
    """
    Serializer for creating a new Patient instance.

    The clinician field is a HiddenField that is not visible in the API request or response.
    However, it is included in the serializer data. By setting the default value to CurrentUserDefault(),
    the authenticated user (clinician) will be automatically assigned to the clinician
    field when creating a new patient.
    """

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
            "created_at",
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


class AssessmentListSerializer(serializers.ModelSerializer):
    patient = serializers.ReadOnlyField(source="patient.full_name")

    class Meta:
        model = Assessment
        fields = [
            "id",
            "patient",
            "assessment_type",
            "assessment_date",
            "final_score",
        ]


class AssessmentCreateSerializer(serializers.ModelSerializer):
    clinician = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Assessment
        fields = [
            "clinician",
            "assessment_type",
            "assessment_date",
            "final_score",
        ]


class AssessmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = [
            "assessment_type",
            "assessment_date",
            "final_score",
        ]
