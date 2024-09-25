from django_filters import ChoiceFilter, DateFromToRangeFilter, FilterSet

from .models import Assessment, Patient

Genders = [
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
]

Assessment_type = [
    ("cognitive", "Cognitive Status"),
    ("physical", "Physical Ability"),
    ("mental", "Mental Health"),
    ("emotional", "Emotional Well-being"),
]


class GenderFilter(FilterSet):
    gender = ChoiceFilter(choices=Genders)

    class Meta:
        model = Patient
        fields = ["gender"]


class AssessmentTypeFilter(FilterSet):
    assessment_type = ChoiceFilter(choices=Assessment_type)
    assessment_date = DateFromToRangeFilter()

    class Meta:
        model = Assessment
        fields = ["assessment_type", "assessment_date", "patient"]
