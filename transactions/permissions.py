from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Object-level permission: only the owner can access the transaction.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id
