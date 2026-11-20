from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Course, Lesson, Module, Track


class BorradoresTests(TestCase):
    def setUp(self):
        track = Track.objects.create(name="T", slug="t")
        self.course = Course.objects.create(
            track=track, title="C", slug="c", summary="s", description="d", is_published=True
        )
        module = Module.objects.create(course=self.course, title="M", order=1)
        self.publicada = Lesson.objects.create(module=module, title="Pub", slug="pub", is_free_preview=True)
        self.borrador = Lesson.objects.create(
            module=module, title="Borr", slug="borr", is_free_preview=True, is_draft=True
        )
        User = get_user_model()
        self.staff = User.objects.create_user(username="staff", email="s@example.com", password="x-Clave-123")
        self.staff.is_staff = True
        self.staff.save()

    def test_alumno_no_ve_borrador(self):
        self.assertEqual(self.client.get(self.borrador.get_absolute_url()).status_code, 404)
        r = self.client.get(self.course.get_absolute_url())
        self.assertContains(r, "Pub")
        self.assertNotContains(r, "Borr")
        self.assertEqual(self.course.lesson_count, 1)

    def test_staff_ve_borrador(self):
        self.client.force_login(self.staff)
        r = self.client.get(self.borrador.get_absolute_url())
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Borrador")

    def test_curso_no_publicado_solo_staff(self):
        self.course.is_published = False
        self.course.save()
        self.assertEqual(self.client.get(self.course.get_absolute_url()).status_code, 404)
        self.assertEqual(self.client.get(self.publicada.get_absolute_url()).status_code, 404)
        self.client.force_login(self.staff)
        self.assertEqual(self.client.get(self.course.get_absolute_url()).status_code, 200)

    def test_youtube_id(self):
        les = Lesson(video_url="https://youtu.be/dQw4w9WgXcQ")
        self.assertEqual(les.youtube_id, "dQw4w9WgXcQ")
        les.video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=3"
        self.assertEqual(les.youtube_id, "dQw4w9WgXcQ")
