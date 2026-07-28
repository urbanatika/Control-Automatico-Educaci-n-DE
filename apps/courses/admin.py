from django.contrib import admin

from .models import Course, Lesson, Module, Track


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    prepopulated_fields = {"slug": ("title",)}


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["order"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "track", "level", "is_published", "order"]
    list_filter = ["track", "level", "is_published"]
    search_fields = ["title", "summary"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "order"]
    list_filter = ["course"]
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["title", "module", "duration_minutes", "is_free_preview", "order"]
    list_filter = ["module__course", "is_free_preview"]
    prepopulated_fields = {"slug": ("title",)}
