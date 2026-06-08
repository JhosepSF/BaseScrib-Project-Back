from django.urls import reverse
from rest_framework.test import APITestCase
from core.models import User, StudentProfile, Classroom


class CoreAPITest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')
        self.teacher = User.objects.create_user(username='teacher1', password='teacherpass', role=User.TEACHER)
        self.student = User.objects.create_user(username='student1', password='studentpass', role=User.STUDENT)
        self.classroom = Classroom.objects.create(name='Class A', grade='4', section='A', teacher=self.teacher)
        StudentProfile.objects.create(user=self.student, classroom=self.classroom, level='A1', avatar='avatar1')

    def get_token(self, username, password):
        return self.client.post('/api/auth/token/', {'username': username, 'password': password}, format='json')

    def test_token_obtain(self):
        resp = self.get_token('student1', 'studentpass')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access', resp.data)

    def test_users_me(self):
        resp = self.get_token('student1', 'studentpass')
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        resp = self.client.get('/api/users/me/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['username'], 'student1')

    def test_student_profile_me(self):
        resp = self.get_token('student1', 'studentpass')
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        resp = self.client.get('/api/student-profiles/me/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['user'], self.student.id)

    def test_teacher_can_list_profiles(self):
        resp = self.get_token('teacher1', 'teacherpass')
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        resp = self.client.get('/api/student-profiles/')
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.data), 1)
