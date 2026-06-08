from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import (
    User,
    Classroom,
    StudentProfile,
    TeacherProfile,
    Level,
    Mission,
    Activity,
    Question,
    AnswerOption,
    WritingSubmission,
    CoinTransaction,
    UnlockCode,
    PrePostTest,
    Observation,
    EngagementMetric,
    TrackingEvent,
    Room,
)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Role & System', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Gamification', {'fields': ('coins', 'xp')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Personal info', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email'),
        }),
        ('Role Assignment', {
            'classes': ('wide',),
            'fields': ('role', 'is_staff', 'is_superuser'),
            'description': '<p style="color: #666; margin: 10px 0;"><strong>Role:</strong> Select "teacher" or "student". ' \
                          'Staff/Superuser will have admin access.</p>',
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-create StudentProfile or TeacherProfile based on role."""
        super().save_model(request, obj, form, change)
        
        # Create associated profile if it doesn't exist
        if obj.role == User.STUDENT:
            StudentProfile.objects.get_or_create(user=obj)
        elif obj.role == User.TEACHER:
            TeacherProfile.objects.get_or_create(user=obj)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'section', 'teacher')
    search_fields = ('name', 'grade', 'section')
    list_filter = ('grade', 'section')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'classroom', 'level', 'avatar')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('level', 'classroom')
    readonly_fields = ('user',)
    
    fieldsets = (
        ('User Info', {'fields': ('user',)}),
        ('Profile', {'fields': ('classroom', 'level', 'avatar')}),
        ('Missions', {'fields': ('unlocked_missions',)}),
    )
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'get_classrooms_count')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('user',)
    
    fieldsets = (
        ('User Info', {'fields': ('user',)}),
        ('Profile', {'fields': ('bio',)}),
    )
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    
    def get_classrooms_count(self, obj):
        return Classroom.objects.filter(teacher=obj.user).count()
    get_classrooms_count.short_description = 'Classrooms'


admin.site.register(TeacherProfile, TeacherProfileAdmin)
admin.site.register(Level)
admin.site.register(Mission)
admin.site.register(Activity)
admin.site.register(Question)
admin.site.register(AnswerOption)
admin.site.register(WritingSubmission)
admin.site.register(CoinTransaction)
admin.site.register(UnlockCode)


@admin.register(PrePostTest)
class PrePostTestAdmin(admin.ModelAdmin):
    list_display = ('student', 'test_type', 'score', 'created_at')
    list_filter = ('test_type',)


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ('student', 'observer', 'session_date')
    search_fields = ('student__username', 'observer__username')


@admin.register(EngagementMetric)
class EngagementMetricAdmin(admin.ModelAdmin):
    list_display = ('student', 'metric', 'value', 'recorded_at')
    list_filter = ('metric',)


@admin.register(TrackingEvent)
class TrackingEventAdmin(admin.ModelAdmin):
    list_display = ('student', 'event_type', 'created_at', 'duration')
    list_filter = ('event_type',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'key', 'teacher', 'created_at', 'is_active')
    search_fields = ('name', 'code', 'key', 'teacher__username')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('code', 'key', 'created_at')
