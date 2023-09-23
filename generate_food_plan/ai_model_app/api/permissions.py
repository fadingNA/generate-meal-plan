from rest_framework import permissions

class isAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.group.filter(name='admin'))
    

class DenyAny(permissions.BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False