from rest_framework import permissions


class IsOwner(permissions.IsAuthenticated):
    """
    Custom permission to only allow clinicians to access their own patients or assessments.
    """

    def has_object_permission(self, request, view, obj):
        return obj.clinician == request.user
