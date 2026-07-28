from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("", views.CatalogView.as_view(), name="catalog"),
    path("<slug:slug>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("<slug:course_slug>/<slug:lesson_slug>/", views.lesson_detail, name="lesson_detail"),
]
