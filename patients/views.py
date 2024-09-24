from django.http import Http404
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from patients.models import Patient

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
        Override the update method to ensure that the response uses the correct serializer.

        By default, the update method returns data using the PatientUpdateSerializer, which
        excludes certain fields such as 'full_name' and 'age'. To address this, we use the
        PatientUpdateSerializer to handle the update process, but after the update, we return
        the full patient details in the response using the PatientDetailSerializer. This ensures
        that the response includes all relevant fields.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = PatientUpdateSerializer(
            instance, data=request.data, partial=partial
        )

        # Validate and update the patient
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Return the full details with PatientDetailSerializer
        detail_serializer = PatientDetailSerializer(instance)
        return Response(detail_serializer.data, status=status.HTTP_200_OK)
