from django.urls import path

from patients.views import (AssessmentCreateAPIView, AssessmentDetailAPIView,
                            AssessmentListAPIView,
                            PatientAssessmentDetailAPIView,
                            PatientAssessmentListAPIView, PatientDetailAPIView,
                            PatientListCreateAPIView)

urlpatterns = [
    path("patient/", PatientListCreateAPIView.as_view()),
    path("patient/<int:pk>/", PatientDetailAPIView.as_view()),
    path("patient/<int:pk>/assessment/", PatientAssessmentListAPIView.as_view()),
    path(
        "patient/<int:patient_pk>/assessment/<int:assessment_pk>/",
        PatientAssessmentDetailAPIView.as_view(),
    ),
    path("patient/<int:pk>/assessment/create", AssessmentCreateAPIView.as_view()),
    path("assessment/", AssessmentListAPIView.as_view()),
    path("assessment/<int:pk>/", AssessmentDetailAPIView.as_view()),
]
