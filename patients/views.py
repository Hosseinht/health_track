from django.contrib.postgres.search import SearchVector
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .filters import AssessmentTypeFilter, GenderFilter
from .models import Address, Assessment, Patient
from .permissions import IsOwner
from .serializers import (
    AssessmentCreateSerializer,
    AssessmentDetailSerializer,
    AssessmentListSerializer,
    PatientCreateSerializer,
    PatientDetailSerializer,
    PatientListSerializer,
    PatientUpdateSerializer,
)


# Create your views here.
class PatientListCreateAPIView(generics.ListCreateAPIView):
    """
    Handles listing and creating patients.

    This view provides a list of patients for the authenticated clinician and allows creating new patients.
    """

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # search_fields = ["name", "pseudonym"]
    ordering_fields = ["date_of_birth", "created_at"]
    filterset_class = GenderFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PatientListSerializer
        elif self.request.method == "POST":
            return PatientCreateSerializer

    def get_queryset(self):
        """
        Retrieves a queryset of patients associated with the current clinician.

        If a search query is provided, the queryset is filtered to include only patients
        whose names match the search query.
        """
        clinician = self.request.user
        query = self.request.query_params.get("search", None)
        patient = Patient.objects.filter(clinician=clinician).select_related(
            "clinician",
            "address",
        )
        if query:
            search_patient = patient.annotate(
                search=SearchVector("first_name", "last_name"),
            ).filter(clinician=clinician, search=query)

            return search_patient
        return patient

    def perform_create(self, serializer):
        """
        Address is a nested serializer in the PatientCreateSerializer. to create a new patient
        we also need to manage the patient address and add an address for the patient.
        """
        patient_data = serializer.validated_data
        address_data = patient_data.pop("address", None)

        if address_data:
            # Address needs to be created separately, so we remove the address from input data
            # and create an address then add it to the patient
            address = Address.objects.create(**address_data)
            patient_data["address"] = address

        serializer.save(**patient_data)


class PatientDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates, or deletes a patient instance.

    This view requires authentication and will only return patients that are
    associated with the clinician making the request.
    """

    permission_classes = [IsOwner]

    def get_object(self):
        """
        Returns the patient instance for the given primary key.

        It checks if the clinician has permission for this patient and also if the patient exists.
        """

        try:
            patient = Patient.objects.select_related("clinician").get(
                pk=self.kwargs["pk"]
            )
            self.check_object_permissions(self.request, patient)
            return patient
        except Patient.DoesNotExist:
            raise NotFound("Patient not found.")

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return PatientUpdateSerializer
        return PatientDetailSerializer

    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        """
        Because address is a nested serializer in the PatientUpdateSerializer we need to override the update
        method and manage the address update
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = PatientUpdateSerializer(
            instance, data=request.data, partial=partial
        )

        serializer.is_valid(raise_exception=True)
        patient_data = serializer.validated_data
        address_data = patient_data.pop("address", None)

        # Update the address (if provided)
        if address_data:
            # here we use .items() to get a list of key values in the serialized data(address)
            # and then use setattr to set these key(attr) value to the model instance(address)
            for attr, value in address_data.items():
                setattr(instance.address, attr, value)
            instance.address.save()

        # Update the patient instance fields
        for attr, value in patient_data.items():
            setattr(instance, attr, value)

        instance.save()

        detail_serializer = PatientDetailSerializer(instance)
        return Response(detail_serializer.data, status=status.HTTP_200_OK)


class AssessmentListAPIView(generics.ListAPIView):
    """
    This view provides a list of patients for the authenticated clinician
    """

    serializer_class = AssessmentListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # search_fields = ["name", "pseudonym"]
    ordering_fields = [
        "assessment_date",
        "assessment_type",
        "patient",
        "final_score",
    ]
    filterset_class = AssessmentTypeFilter

    def get_queryset(self):
        return Assessment.objects.select_related("clinician", "patient").filter(
            clinician=self.request.user
        )


class AssessmentCreateAPIView(generics.CreateAPIView):
    """
    Handles creating assessments for a patient.

    This view creates a new assessment instance for a patient with the given primary key.

    """

    serializer_class = AssessmentCreateSerializer

    def perform_create(self, serializer):
        patient_pk = self.kwargs["pk"]
        try:
            patient = Patient.objects.get(pk=patient_pk)
        except Patient.DoesNotExist:
            raise NotFound("Patient not found.")
        serializer.save(patient=patient)


class AssessmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting assessments.

    This view provides a detailed view of an assessment instance and allows updating and deleting the assessment.
    """

    permission_classes = [IsOwner]
    serializer_class = AssessmentDetailSerializer

    def get_object(self):
        """
        Returns the assessment instance for the given primary key.

        It checks if the clinician has permission for this assessment and also if the assessment exists.
        """
        pk = self.kwargs["pk"]
        try:
            assessment = Assessment.objects.select_related("clinician", "patient").get(
                pk=pk
            )
            self.check_object_permissions(self.request, assessment)

            return assessment
        except Assessment.DoesNotExist:
            raise NotFound("Assessment not found.")


class PatientAssessmentListAPIView(generics.ListAPIView):
    """
    Handles listing assessments for a patient.

    This view provides a list of assessment instances for a patient with the given primary key,
    filtered by the authenticated clinician.
    """

    serializer_class = AssessmentListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # search_fields = ["name", "pseudonym"]
    ordering_fields = [
        "assessment_date",
        "assessment_type",
        "final_score",
    ]
    filterset_class = AssessmentTypeFilter

    def get_queryset(self):
        clinician = self.request.user
        patient_pk = self.kwargs["pk"]
        return Assessment.objects.filter(clinician=clinician, patient_id=patient_pk)


class PatientAssessmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves the assessment instance with the given primary key for the patient.

    Retrieves the assessment instance with the given primary key for the patient with
    the given primary key, checks the object permissions, and returns the assessment instance.
    """

    permission_classes = [IsOwner]
    serializer_class = AssessmentDetailSerializer

    def get_object(self):
        """
        Retrieves a single assessment instance related to a specific patient
        using the patient ID and assessment ID.
        """
        patient_pk = self.kwargs["patient_pk"]
        assessment_pk = self.kwargs["assessment_pk"]
        try:
            assessment = Assessment.objects.select_related("clinician", "patient").get(
                patient__pk=patient_pk, pk=assessment_pk
            )

            self.check_object_permissions(self.request, assessment)
            # check if the clinician has permission

            return assessment
        except Assessment.DoesNotExist:
            raise NotFound("Assessment not found.")
