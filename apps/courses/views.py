from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from apps.subscriptions.access import has_active_subscription

from .models import Course, Lesson, Track


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
        return Course.objects.filter(is_published=True).prefetch_related("modules__lessons")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_access"] = has_active_subscription(self.request.user)
        return context


def lesson_detail(request, course_slug, lesson_slug):
    lesson = get_object_or_404(
        Lesson.objects.select_related("module__course"),
        slug=lesson_slug,
        module__course__slug=course_slug,
    )
    course = lesson.course
    has_access = has_active_subscription(request.user)
    can_watch = has_access or lesson.is_free_preview

    return render(
        request,
        "courses/lesson_detail.html",
        {
            "lesson": lesson,
            "course": course,
            "modules": course.modules.prefetch_related("lessons").all(),
            "can_watch": can_watch,
            "has_access": has_access,
        },
    )
