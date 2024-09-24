from django.urls import path

from patients.views import (PatientCreateView, PatientDetailView,
                            PatientListView)

urlpatterns = [
    path("patient/", PatientListView.as_view()),
    path("patient/create/", PatientCreateView.as_view()),
    path("patient/<int:pk>/", PatientDetailView.as_view()),
]
