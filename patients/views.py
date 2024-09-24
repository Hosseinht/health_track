from django.http import Http404
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from patients.models import Address, Patient

from .serializers import (PatientCreateSerializer, PatientDetailSerializer,
                          PatientListSerializer, PatientUpdateSerializer)


# Create your views here.
class PatientListView(generics.ListAPIView):
    """
    Returns a list of patients for the currently authenticated clinician.

    This view requires authentication and will only return patients that are
    associated with the clinician making the request.
    """

    serializer_class = PatientListSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You are not authenticated")
        # We need to check if the user authenticated or not, because otherwise django
        return Patient.objects.filter(clinician=self.request.user).select_related(
            "clinician"
        )


class PatientCreateView(generics.CreateAPIView):
    """
    This view is responsible for creating patients
    """

    queryset = Patient.objects.all()
    serializer_class = PatientCreateSerializer

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


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves, updates, or deletes a patient instance.

    This view requires authentication and will only return patients that are
    associated with the clinician making the request.
    """

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You are not authenticated")

        return Patient.objects.filter(clinician=self.request.user).select_related(
            "clinician"
        )

    def get_serializer_class(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return PatientUpdateSerializer
        return PatientDetailSerializer

    def get_object(self):
        """
        Returns the patient instance for the given primary key.

        If the patient instance does not exist or if the clinician does not have
        access to the patient, this method raises a PermissionDenied exception.
        """
        try:
            return super().get_object()
        except Http404:
            raise PermissionDenied("You do not have access to this patient")

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
