from rest_framework import permissions

class RoleBasedPermission(permissions.BasePermission):
    """
    Permission check for roles
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated first
        if not request.user or not request.user.is_authenticated:
            return False

        # Check if the user tries to access their own data or they are an admin
        is_own_data = request.user.username == view.kwargs.get('username')
        is_admin = request.user.privilege == 'admin'

        # `viewer` role can only use GET method and only for their own data
        if request.user.privilege == 'viewer':
            return request.method == 'GET'

        # `manager` roles can use all methods but only for their own data
        elif request.user.privilege == 'manager':
            return True

        # `admin` role can use all methods for all users
        elif is_admin:
            return True

        return False
