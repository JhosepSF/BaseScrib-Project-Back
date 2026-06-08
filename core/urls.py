from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from .views import (
    UserViewSet,
    StudentViewSet,
    TeacherViewSet,
    ClassroomViewSet,
    StudentProfileViewSet,
    TeacherProfileViewSet,
    LevelViewSet,
    MissionViewSet,
    ActivityViewSet,
    QuestionViewSet,
    AnswerOptionViewSet,
    WritingSubmissionViewSet,
    CoinTransactionViewSet,
    UnlockCodeViewSet,
    PrePostTestViewSet,
    ObservationViewSet,
    EngagementMetricViewSet,
    TrackingEventViewSet,
    RoomViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'students', StudentViewSet, basename='student')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'classrooms', ClassroomViewSet)
router.register(r'student-profiles', StudentProfileViewSet)
router.register(r'teacher-profiles', TeacherProfileViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'missions', MissionViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answer-options', AnswerOptionViewSet)
router.register(r'writing-submissions', WritingSubmissionViewSet)
router.register(r'coin-transactions', CoinTransactionViewSet)
router.register(r'unlock-codes', UnlockCodeViewSet)
router.register(r'prepost-tests', PrePostTestViewSet)
router.register(r'observations', ObservationViewSet)
router.register(r'engagement-metrics', EngagementMetricViewSet)
router.register(r'tracking-events', TrackingEventViewSet)
router.register(r'rooms', RoomViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
