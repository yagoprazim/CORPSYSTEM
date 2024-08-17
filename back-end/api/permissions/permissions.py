from rest_framework.permissions import BasePermission

class IsVendor(BasePermission):
     def has_permission(self, request, view):     
        if request.method == 'GET':
            return True
        
        if hasattr(request.user, 'vendor'):
            return True
        
        return False