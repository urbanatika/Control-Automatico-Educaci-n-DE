from django.db import models
from django.urls import reverse


class Track(models.Model):
    """Un eje temático del programa (ej. Control Lineal, Recorrido Histórico)."""

    name = models.CharField("nombre", max_length=120)
    slug = models.SlugField("slug", unique=True)
    description = models.TextField("descripción", blank=True)
    icon = models.CharField(
        "ícono", max_length=50, blank=True, help_text="Nombre del ícono SVG en static/images/icons/"
    )
    order = models.PositiveIntegerField("orden", default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "eje temático"
        verbose_name_plural = "ejes temáticos"

    def __str__(self):
        return self.name


class Course(models.Model):
    class Level(models.TextChoices):
        BASICO = "basico", "Básico"
        INTERMEDIO = "intermedio", "Intermedio"
        AVANZADO = "avanzado", "Avanzado"

    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="courses", verbose_name="eje temático")
    title = models.CharField("título", max_length=200)
    slug = models.SlugField("slug", unique=True)
    summary = models.CharField("resumen", max_length=300)
    description = models.TextField("descripción")
    level = models.CharField("nivel", max_length=20, choices=Level.choices, default=Level.BASICO)
    thumbnail = models.ImageField("miniatura", upload_to="courses/thumbnails/", blank=True, null=True)
    order = models.PositiveIntegerField("orden", default=0)
    is_published = models.BooleanField("publicado", default=True)
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        ordering = ["track__order", "order", "title"]
        verbose_name = "curso"
        verbose_name_plural = "cursos"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:course_detail", kwargs={"slug": self.slug})

    @property
    def lesson_count(self):
        return Lesson.objects.filter(module__course=self).count()

    @property
    def total_duration_minutes(self):
        return Lesson.objects.filter(module__course=self).aggregate(
            total=models.Sum("duration_minutes")
        )["total"] or 0


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules", verbose_name="curso")
    title = models.CharField("título", max_length=200)
    order = models.PositiveIntegerField("orden", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "módulo"
        verbose_name_plural = "módulos"

    def __str__(self):
        return f"{self.course.title} — {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons", verbose_name="módulo")
    title = models.CharField("título", max_length=200)
    slug = models.SlugField("slug")
    description = models.TextField("descripción", blank=True)
    vimeo_id = models.CharField(
        "ID de video en Vimeo",
        max_length=50,
        blank=True,
        help_text="Ej: 123456789 (de un video privado/con dominio restringido en Vimeo)",
    )
    duration_minutes = models.PositiveIntegerField("duración (min)", default=0)
    order = models.PositiveIntegerField("orden", default=0)
    is_free_preview = models.BooleanField(
        "vista previa gratuita", default=False, help_text="Visible sin suscripción"
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "lección"
        verbose_name_plural = "lecciones"
        unique_together = ["module", "slug"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "courses:lesson_detail",
            kwargs={"course_slug": self.module.course.slug, "lesson_slug": self.slug},
        )

    @property
    def course(self):
        return self.module.course
