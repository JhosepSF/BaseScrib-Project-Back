from typing import TYPE_CHECKING

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    if TYPE_CHECKING:
        from django.db.models.query import QuerySet

        joined_rooms: "QuerySet[Room]"
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (ADMIN, 'Administrator'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
    coins = models.PositiveIntegerField(default=0)
    xp = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.username} ({self.role})'


class Classroom(models.Model):
    name = models.CharField(max_length=128)
    grade = models.CharField(max_length=32)
    section = models.CharField(max_length=32)
    teacher = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, limit_choices_to={'role': User.TEACHER})

    def __str__(self):
        return f'{self.grade} {self.section} - {self.name}'


class StudentProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='student_profile')
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    level = models.CharField(max_length=64, blank=True)
    unlocked_missions = models.ManyToManyField('Mission', blank=True, related_name='unlocked_by')
    avatar = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.user.username


class TeacherProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='teacher_profile')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Level(models.Model):
    code = models.CharField(max_length=32, unique=True)
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Mission(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='missions')
    order = models.PositiveIntegerField(default=0)
    unlock_code = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ['level', 'order']

    def __str__(self):
        return self.title


class Activity(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    is_open = models.BooleanField(default=False)
    max_score = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f'{self.mission.title} - {self.title}'


class Question(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    is_free_text = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:60]


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=256)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class WritingSubmission(models.Model):
    id: int
    student = models.ForeignKey('User', on_delete=models.CASCADE, limit_choices_to={'role': User.STUDENT})
    mission = models.ForeignKey(Mission, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    # Tipado para herramientas estáticas (pylance/mypy) sin tocar el modelo real
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        id: int

    def __str__(self):
        return f'Submission {self.id} by {self.student.username}'


class CoinTransaction(models.Model):
    student = models.ForeignKey('User', on_delete=models.CASCADE, limit_choices_to={'role': User.STUDENT})
    amount = models.IntegerField()
    reason = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.username}: {self.amount}'


class UnlockCode(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='unlock_codes')
    code = models.CharField(max_length=64, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class PrePostTest(models.Model):
    TEST_TYPE_CHOICES = [('pre', 'Pretest'), ('post', 'Posttest')]
    student = models.ForeignKey('User', on_delete=models.CASCADE, limit_choices_to={'role': User.STUDENT})
    test_type = models.CharField(max_length=8, choices=TEST_TYPE_CHOICES)
    score = models.FloatField(null=True, blank=True)
    raw_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.username} - {self.test_type} - {self.created_at.date()}'


class Observation(models.Model):
    observer = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='observations_made')
    student = models.ForeignKey('User', on_delete=models.CASCADE, limit_choices_to={'role': User.STUDENT}, related_name='observations')
    session_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    criteria = models.JSONField(blank=True, null=True)

    # Tipado para herramientas estáticas (pylance/mypy) sin cambiar el modelo real
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        id: int

    def __str__(self):
        return f'Observation {self.id} for {self.student.username}'


class EngagementMetric(models.Model):
    student = models.ForeignKey('User', on_delete=models.CASCADE, limit_choices_to={'role': User.STUDENT})
    metric = models.CharField(max_length=128)  # e.g., 'time_on_task', 'attempts', 'joy'
    value = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.username} - {self.metric} = {self.value}'


class TrackingEvent(models.Model):
    student = models.ForeignKey('User', on_delete=models.CASCADE, limit_choices_to={'role': User.STUDENT})
    event_type = models.CharField(max_length=128)  # e.g., 'mission_start', 'mission_complete'
    metadata = models.JSONField(blank=True, null=True)
    duration = models.FloatField(null=True, blank=True)  # seconds
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.username} - {self.event_type} @ {self.created_at}'


class Room(models.Model):
    teacher = models.ForeignKey('User', on_delete=models.CASCADE, limit_choices_to={'role': User.TEACHER}, related_name='rooms')
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=6, unique=True)
    key = models.CharField(max_length=8, unique=True)
    students = models.ManyToManyField('User', limit_choices_to={'role': User.STUDENT}, related_name='joined_rooms', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} ({self.code}) - {self.teacher.username}'
