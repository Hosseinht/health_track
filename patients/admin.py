from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedTabularInline  # noqa

from .models import Address, Answer, Assessment, Patient, Question


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


class AnswerInline(NestedTabularInline):
    model = Answer
    extra = 1
    max_num = 1


class QuestionInline(NestedTabularInline):
    model = Question
    extra = 1
    inlines = [AnswerInline]


class AssessmentAdmin(NestedModelAdmin):
    list_display = ["clinician", "patient", "assessment_type", "final_score"]
    search_fields = ["clinician", "patient"]
    list_filter = ["clinician", "patient", "assessment_type"]
    inlines = [QuestionInline]


# Register your models here.
admin.site.register(Address, AddressAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Assessment, AssessmentAdmin)
