from rest_framework import permissions

class isUserAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role == "user":
            return True
        return False
    
class isGuestAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role == "guest":
            return True
        return False
    
class isGuestOrUserAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role == "guest" or request.user.role == "user":
            return True
        return False