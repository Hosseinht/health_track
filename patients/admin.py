from django.contrib import admin

from .models import Address, Assessment, Patient


class AddressAdmin(admin.ModelAdmin):
    list_display = ["get_patient_name"]

    def get_patient_name(self, obj):
        return (obj.patient.full_name + "'s address") if obj.patient else "No Patient"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("patient")
        return queryset


class PatientAdmin(admin.ModelAdmin):
    list_display = ["full_name", "gender", "phone_number", "age"]
    search_fields = ["full_name"]
    list_filter = ["first_name", "last_name", "gender"]


class AssessmentAdmin(admin.ModelAdmin):
    list_display = ["clinician", "patient", "assessment_type", "final_score"]
    search_fields = ["clinician", "patient"]
    list_filter = ["clinician", "patient", "assessment_type"]


admin.site.register(Address, AddressAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Assessment, AssessmentAdmin)
