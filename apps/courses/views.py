from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from apps.subscriptions.access import has_active_subscription

from .models import Course, Lesson, Track


def is_staff(user) -> bool:
    return bool(user and user.is_authenticated and user.is_staff)


def visible_lessons(user):
    """Lecciones que puede ver el usuario: el personal (staff) ve también los borradores."""
    qs = Lesson.objects.all()
    return qs if is_staff(user) else qs.filter(is_draft=False)


class CatalogView(ListView):
    model = Track
    template_name = "courses/catalog.html"
    context_object_name = "tracks"

    def get_queryset(self):
        return Track.objects.prefetch_related("courses").all()


class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        qs = Course.objects.all() if is_staff(self.request.user) else Course.objects.filter(is_published=True)
        return qs.prefetch_related(Prefetch("modules__lessons", queryset=visible_lessons(self.request.user)))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_access"] = has_active_subscription(self.request.user) or is_staff(self.request.user)
        return context


def lesson_detail(request, course_slug, lesson_slug):
    lesson = get_object_or_404(
        Lesson.objects.select_related("module__course").prefetch_related("attachments", "quiz_questions__choices"),
        slug=lesson_slug,
        module__course__slug=course_slug,
    )
    course = lesson.course
    staff = is_staff(request.user)
    if (lesson.is_draft or not course.is_published) and not staff:
        raise Http404
    has_access = has_active_subscription(request.user) or staff
    can_watch = has_access or lesson.is_free_preview

    return render(
        request,
        "courses/lesson_detail.html",
        {
            "lesson": lesson,
            "course": course,
            "modules": course.modules.prefetch_related(
                Prefetch("lessons", queryset=visible_lessons(request.user))
            ).all(),
            "can_watch": can_watch,
            "has_access": has_access,
        },
    )
