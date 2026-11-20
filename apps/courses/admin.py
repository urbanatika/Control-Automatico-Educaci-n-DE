from django.contrib import admin

from .models import Course, Lesson, LessonAttachment, Module, QuizChoice, QuizQuestion, Track


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ["title", "slug", "order", "duration_minutes", "is_free_preview", "is_draft"]
    prepopulated_fields = {"slug": ("title",)}


class LessonAttachmentInline(admin.TabularInline):
    model = LessonAttachment
    extra = 0


class QuizQuestionInline(admin.StackedInline):
    model = QuizQuestion
    extra = 0
    show_change_link = True


class QuizChoiceInline(admin.TabularInline):
    model = QuizChoice
    extra = 0


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
    list_display = ["title", "module", "duration_minutes", "is_free_preview", "is_draft", "order"]
    list_filter = ["module__course", "is_free_preview", "is_draft"]
    list_editable = ["is_draft"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonAttachmentInline, QuizQuestionInline]
    fieldsets = [
        (None, {"fields": ["module", "title", "slug", "description", "order", "duration_minutes"]}),
        ("Video", {"fields": ["vimeo_id", "video_url", "video_file", "subtitles_file", "thumbnail"]}),
        ("Visibilidad", {"fields": ["is_draft", "is_free_preview", "source_key"]}),
    ]


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ["text", "lesson", "order"]
    list_filter = ["lesson__module__course"]
    inlines = [QuizChoiceInline]
