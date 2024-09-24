from rest_framework import permissions


class IsClinician(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.clinician == request.user
