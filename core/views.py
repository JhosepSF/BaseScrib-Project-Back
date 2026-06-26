from typing import cast

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsTeacherOrAdmin, IsProfileOwnerOrTeacher, IsOwnerOrTeacherForClassroom
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
from .serializers import (
    UserSerializer,
    ClassroomSerializer,
    StudentProfileSerializer,
    TeacherProfileSerializer,
    LevelSerializer,
    MissionSerializer,
    ActivitySerializer,
    QuestionSerializer,
    AnswerOptionSerializer,
    WritingSubmissionSerializer,
    CoinTransactionSerializer,
    UnlockCodeSerializer,
    PrePostTestSerializer,
    ObservationSerializer,
    EngagementMetricSerializer,
    TrackingEventSerializer,
    RoomSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def award_rewards(self, request):
        user = request.user
        coins = int(request.data.get('coins', 0))
        xp = int(request.data.get('xp', 0))
        if coins > 0:
            user.coins += coins
        if xp > 0:
            user.xp += xp
        user.save()
        return Response({
            'status': 'rewards awarded',
            'coins': user.coins,
            'xp': user.xp
        })

    @action(detail=False, methods=['post'])
    def unlock_outfit(self, request):
        """Spend coins to unlock a new outfit."""
        OUTFIT_COSTS = {
            'm_base': 0, 'f_base': 0,
            'm_explorer': 30, 'f_explorer': 30,
            'm_tech': 50, 'f_scientist': 50,
            'm_commander': 100, 'f_commander': 100,
        }
        outfit_id = request.data.get('outfit_id', '')
        if outfit_id not in OUTFIT_COSTS:
            return Response({'error': 'Outfit inválido'}, status=400)

        user = cast(User, request.user)
        if user.role != User.STUDENT:
            return Response({'error': 'Solo estudiantes pueden canjear outfits'}, status=403)

        try:
            profile = user.student_profile
        except StudentProfile.DoesNotExist:
            profile = StudentProfile.objects.create(user=user, unlocked_outfits=['m_base', 'f_base'])

        unlocked = list(profile.unlocked_outfits or ['m_base', 'f_base'])
        if outfit_id in unlocked:
            return Response({'error': 'Ya tienes este outfit desbloqueado'}, status=400)

        cost = OUTFIT_COSTS[outfit_id]
        if user.coins < cost:
            return Response({'error': f'Monedas insuficientes. Necesitas {cost} 🪙, tienes {user.coins} 🪙'}, status=400)

        # Deduct coins and unlock
        user.coins -= cost
        user.save()
        unlocked.append(outfit_id)
        profile.unlocked_outfits = unlocked
        profile.save()

        # Record transaction
        CoinTransaction.objects.create(student=user, amount=-cost, reason=f'Outfit desbloqueado: {outfit_id}')

        return Response({
            'status': 'outfit unlocked',
            'outfit_id': outfit_id,
            'coins': user.coins,
            'unlocked_outfits': unlocked,
        })

    @action(detail=False, methods=['post'])
    def select_outfit(self, request):
        """Change the active selected outfit (must be already unlocked)."""
        outfit_id = request.data.get('outfit_id', '')
        user = cast(User, request.user)

        try:
            profile = user.student_profile
        except StudentProfile.DoesNotExist:
            return Response({'error': 'Perfil no encontrado'}, status=404)

        unlocked = list(profile.unlocked_outfits or ['m_base', 'f_base'])
        if outfit_id not in unlocked:
            return Response({'error': 'Outfit no desbloqueado'}, status=403)

        profile.selected_outfit = outfit_id
        profile.save()
        return Response({'status': 'outfit selected', 'selected_outfit': outfit_id})




class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(role=User.STUDENT)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(role=User.TEACHER)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [IsOwnerOrTeacherForClassroom]

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        classroom = self.get_object()
        students = list(classroom.students.select_related('user').all())
        data = [s.user.username for s in students]
        return Response({'students': data})


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.select_related('user', 'classroom').all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsProfileOwnerOrTeacher]

    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            profile = request.user.student_profile
        except StudentProfile.DoesNotExist:
            return Response({}, status=204)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.select_related('user').all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsProfileOwnerOrTeacher]

    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            profile = request.user.teacher_profile
        except TeacherProfile.DoesNotExist:
            return Response({}, status=204)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsTeacherOrAdmin])
    def student_scores(self, request):
        """Return aggregated student scores for the teacher's classes."""
        teacher = cast(User, request.user)
        if teacher.is_superuser:
            student_ids = set(User.objects.filter(role=User.STUDENT).values_list('id', flat=True))
        else:
            # students in teacher's classrooms or rooms
            classrooms = Classroom.objects.filter(teacher=teacher).values_list('students__user__id', flat=True)
            room_students = User.objects.filter(joined_rooms__teacher=teacher).values_list('id', flat=True)
            student_ids = set([sid for sid in classrooms if sid]) | set(room_students)

        # aggregate average writing submission score and prepost test score per student
        from django.db.models import Avg

        writing_avgs = WritingSubmission.objects.filter(student__id__in=student_ids, score__isnull=False).values('student__id', 'student__username').annotate(avg_score=Avg('score'))
        prepost_avgs = PrePostTest.objects.filter(student__id__in=student_ids, score__isnull=False).values('student__id').annotate(prepost_avg=Avg('score'))

        data = {}
        for w in writing_avgs:
            sid = w['student__id']
            data[sid] = {'id': sid, 'username': w['student__username'], 'writing_avg': float(w['avg_score'])}
        for p in prepost_avgs:
            sid = p['student__id']
            if sid not in data:
                data[sid] = {'id': sid, 'username': User.objects.get(id=sid).username}
            data[sid]['prepost_avg'] = float(p['prepost_avg'])

        # Also compute per-mission averages for writing submissions
        mission_rows = WritingSubmission.objects.filter(student__id__in=student_ids, score__isnull=False).values('mission__id', 'mission__title').annotate(mission_avg=Avg('score'))
        missions = [{ 'mission_id': m['mission__id'], 'mission_title': m['mission__title'], 'mission_avg': float(m['mission_avg']) } for m in mission_rows if m['mission__id']]

        result = list(data.values())
        return Response({'students': result, 'missions': missions})

    @action(detail=False, methods=['get'], permission_classes=[IsTeacherOrAdmin])
    def engagement(self, request):
        """Return engagement metrics (time_on_task) per student for this teacher."""
        teacher = cast(User, request.user)
        if teacher.is_superuser:
            students = User.objects.filter(role=User.STUDENT)
        else:
            # students related to this teacher via rooms
            students = User.objects.filter(joined_rooms__teacher=teacher).distinct()
        from django.db.models import Sum
        rows = EngagementMetric.objects.filter(student__in=students, metric='time_on_task').values('student__id', 'student__username').annotate(total=Sum('value'))
        data = [{ 'id': r['student__id'], 'username': r['student__username'], 'time_on_task_seconds': float(r['total'] or 0) } for r in rows]
        return Response({'engagement': data})

    @action(detail=False, methods=['get'], permission_classes=[IsTeacherOrAdmin])
    def oral_reviews(self, request):
        """Return recent writing submissions for review (pending and reviewed)."""
        teacher = cast(User, request.user)
        if teacher.is_superuser:
            students = User.objects.filter(role=User.STUDENT)
        else:
            students = User.objects.filter(joined_rooms__teacher=teacher).distinct()
        # pagination
        from django.core.paginator import Paginator, EmptyPage
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        qs = WritingSubmission.objects.filter(student__in=students).order_by('-submitted_at')
        paginator = Paginator(qs, page_size)
        try:
            page_obj = paginator.page(page)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        subs = page_obj.object_list
        out = []
        for s in subs:
            out.append({
                'id': s.id,
                'student': s.student.username,
                'mission': s.mission.title if s.mission else None,
                'submitted_at': s.submitted_at.isoformat(),
                'reviewed': s.reviewed,
                'score': s.score,
                'text_preview': (s.text[:200] + '...') if len(s.text) > 200 else s.text,
            })
        return Response({'submissions': out, 'page': page, 'num_pages': paginator.num_pages})


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = [permissions.IsAuthenticated]


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [permissions.IsAuthenticated]


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class AnswerOptionViewSet(viewsets.ModelViewSet):
    queryset = AnswerOption.objects.all()
    serializer_class = AnswerOptionSerializer
    permission_classes = [permissions.IsAuthenticated]


class WritingSubmissionViewSet(viewsets.ModelViewSet):
    queryset = WritingSubmission.objects.all()
    serializer_class = WritingSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[IsTeacherOrAdmin])
    def mark_reviewed(self, request, pk=None):
        """Mark a writing submission as reviewed and optionally set score and feedback.

        POST body: { "reviewed": true, "score": 8, "feedback": "Good job" }
        """
        submission = self.get_object()
        reviewed = request.data.get('reviewed')
        score = request.data.get('score')
        feedback = request.data.get('feedback')

        if reviewed is not None:
            submission.reviewed = bool(reviewed)
        if score is not None:
            try:
                val = int(score)
                submission.score = max(0, min(val, 20))
            except Exception:
                pass
        if feedback is not None:
            submission.feedback = str(feedback)

        submission.save()
        serializer = self.get_serializer(submission)
        return Response(serializer.data)


class CoinTransactionViewSet(viewsets.ModelViewSet):
    queryset = CoinTransaction.objects.all()
    serializer_class = CoinTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


class UnlockCodeViewSet(viewsets.ModelViewSet):
    queryset = UnlockCode.objects.all()
    serializer_class = UnlockCodeSerializer
    permission_classes = [permissions.IsAuthenticated]


class PrePostTestViewSet(viewsets.ModelViewSet):
    queryset = PrePostTest.objects.all()
    serializer_class = PrePostTestSerializer
    permission_classes = [permissions.IsAuthenticated]


class ObservationViewSet(viewsets.ModelViewSet):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer
    permission_classes = [IsTeacherOrAdmin]


class EngagementMetricViewSet(viewsets.ModelViewSet):
    queryset = EngagementMetric.objects.all()
    serializer_class = EngagementMetricSerializer
    permission_classes = [permissions.IsAuthenticated]


class TrackingEventViewSet(viewsets.ModelViewSet):
    queryset = TrackingEvent.objects.all()
    serializer_class = TrackingEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # allow students to submit tracking; add server timestamp
        serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[IsTeacherOrAdmin])
    def export_csv(self, request):
        import csv
        from django.http import HttpResponse

        qs = self.get_queryset()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tracking_events.csv"'
        writer = csv.writer(response)
        writer.writerow(['student', 'event_type', 'duration', 'metadata', 'created_at'])
        events = list(qs.select_related('student').all())
        for e in events:
            writer.writerow([e.student.username, e.event_type, e.duration, e.metadata or '', e.created_at.isoformat()])
        return response

    @action(detail=False, methods=['get'], permission_classes=[IsTeacherOrAdmin])
    def export_pdf(self, request):
        # Simple PDF export using reportlab
        from django.http import HttpResponse
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.lib import colors
        import io

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        data = [['student', 'event_type', 'duration', 'created_at']]
        events = list(self.get_queryset().select_related('student').all())
        for e in events:
            data.append([e.student.username, e.event_type, str(e.duration), e.created_at.isoformat()])
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey), ('GRID', (0,0), (-1,-1), 1, colors.black)]))
        doc.build([table])
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        import secrets
        user = cast(User, self.request.user)
        if user.role != User.TEACHER:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Solo docentes pueden crear rooms.')
        code = secrets.token_hex(3).upper()  # 6 chars hex
        key = secrets.token_hex(4).upper()   # 8 chars hex
        serializer.save(teacher=user, code=code, key=key)

    @action(detail=False, methods=['get'])
    def my_rooms(self, request):
        """List rooms created by the teacher or joined by the student."""
        user = cast(User, request.user)
        if user.role == User.TEACHER:
            rooms = Room.objects.filter(teacher=user)
        else:  # STUDENT
            rooms = user.joined_rooms.all()
        
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def join_room(self, request):
        """Join a room using code and key."""
        code = request.data.get('code', '').upper()
        key = request.data.get('key', '').upper()

        try:
            room = Room.objects.get(code=code, key=key, is_active=True)
        except Room.DoesNotExist:
            return Response({'error': 'Código o clave incorrectos'}, status=400)

        user = cast(User, request.user)
        # Add student to room
        if user.role == User.STUDENT:
            room.students.add(user)
            return Response({'message': 'Unido a la room', 'room': RoomSerializer(room).data})
        else:
            return Response({'error': 'Solo estudiantes pueden unirse'}, status=403)
