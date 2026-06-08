from rest_framework import permissions


class IsTeacherOrAdmin(permissions.BasePermission):
    """Allow access only to users with role 'teacher' or admin/superuser."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        role = getattr(request.user, 'role', None)
        return role == 'teacher' or request.user.is_superuser


class IsProfileOwnerOrTeacher(permissions.BasePermission):
    """Allow students to manage their own profile; teachers/admins can view/manage student profiles."""

    def has_permission(self, request, view):
        # Listing profiles: only teachers/admins allowed
        if view.action == 'list':
            role = getattr(request.user, 'role', None)
            return role == 'teacher' or request.user.is_superuser
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj is StudentProfile or TeacherProfile
        if hasattr(obj, 'user'):
            if obj.user == request.user:
                return True
        role = getattr(request.user, 'role', None)
        return role == 'teacher' or request.user.is_superuser


class IsOwnerOrTeacherForClassroom(permissions.BasePermission):
    """Teachers or admins can modify classrooms; students can read."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        role = getattr(request.user, 'role', None)
        return role == 'teacher' or request.user.is_superuser
