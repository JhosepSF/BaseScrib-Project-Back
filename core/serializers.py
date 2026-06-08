from rest_framework import serializers
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


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'coins', 'xp', 'password']
        extra_kwargs = {
            'coins': {'read_only': True},
            'xp': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        if user.role == User.STUDENT:
            StudentProfile.objects.create(user=user)
        elif user.role == User.TEACHER:
            TeacherProfile.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'name', 'grade', 'section', 'teacher']


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'classroom', 'level', 'avatar', 'unlocked_missions']


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ['id', 'user', 'bio']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'code', 'title', 'description', 'order']


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ['id', 'title', 'description', 'level', 'order', 'unlock_code']


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'question', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'activity', 'text', 'is_free_text', 'options']


class ActivitySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'mission', 'title', 'description', 'is_open', 'max_score', 'questions']


class WritingSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WritingSubmission
        fields = ['id', 'student', 'mission', 'text', 'submitted_at', 'reviewed', 'score', 'feedback']



class CoinTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinTransaction
        fields = ['id', 'student', 'amount', 'reason', 'created_at']


class UnlockCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnlockCode
        fields = ['id', 'mission', 'code', 'active']


class PrePostTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrePostTest
        fields = ['id', 'student', 'test_type', 'score', 'raw_data', 'created_at']


class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = ['id', 'observer', 'student', 'session_date', 'notes', 'criteria']


class EngagementMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngagementMetric
        fields = ['id', 'student', 'metric', 'value', 'recorded_at']


class TrackingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingEvent
        fields = ['id', 'student', 'event_type', 'metadata', 'duration', 'created_at']


class RoomSerializer(serializers.ModelSerializer):
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'teacher', 'name', 'code', 'key', 'students', 'students_count', 'created_at', 'is_active']
        read_only_fields = ['teacher', 'code', 'key', 'created_at']

    def get_students_count(self, obj):
        return obj.students.count()
