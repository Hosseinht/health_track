from django.urls import path

from patients.views import (AssessmentCreateAPIView, AssessmentDetailAPIView,
                            AssessmentListAPIView,
                            PatientAssessmentDetailAPIView,
                            PatientAssessmentListAPIView, PatientDetailAPIView,
                            PatientListCreateAPIView)

urlpatterns = [
    path("patient/", PatientListCreateAPIView.as_view(), name="patient-list"),
    path("patient/<int:pk>/", PatientDetailAPIView.as_view(), name="patient-detail"),
    path(
        "patient/<int:pk>/assessment/",
        PatientAssessmentListAPIView.as_view(),
        name="patient-assessment-list",
    ),
    path(
        "patient/<int:patient_pk>/assessment/<int:assessment_pk>/",
        PatientAssessmentDetailAPIView.as_view(),
        name="patient-assessment-detail",
    ),
    path(
        "patient/<int:pk>/assessment/create",
        AssessmentCreateAPIView.as_view(),
        name="patient-assessment-create",
    ),
    path("assessment/", AssessmentListAPIView.as_view(), name="assessment-list"),
    path(
        "assessment/<int:pk>/",
        AssessmentDetailAPIView.as_view(),
        name="assessment-detail",
    ),
]
