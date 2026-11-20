"""Importa una clase producida por el pipeline del curso (carpeta salida/cNN con leccion.json).

Uso:
    python manage.py importar_clase C:\\curso-control\\salida\\c01
    python manage.py importar_clase <carpeta> --curso curso-control-automatico --modulo-titulo "Fundamentos"

- La lección SIEMPRE queda como borrador (is_draft=True): solo la ve el personal (staff).
  Se publica a mano desde el admin, desmarcando «borrador».
- Si el curso no existe, se crea como NO publicado.
- Es idempotente: si ya existe una lección con la misma clave (CA-cNN), se actualiza y se reemplazan
  su video, subtítulos, miniatura, materiales y quiz.
"""
import json
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.courses.models import Course, Lesson, LessonAttachment, Module, QuizChoice, QuizQuestion, Track

CURSO_POR_DEFECTO = {
    "slug": "curso-control-automatico",
    "title": "Control automático: de lo básico al control no lineal",
    "summary": "42 clases en pizarra, con historia, ejercicios y práctica en Arduino/ESP32.",
    "description": (
        "Curso completo de control automático: desde qué es un sistema hasta control no lineal, "
        "MPC, control robusto, adaptativo, difuso y neuronal."
    ),
}


class Command(BaseCommand):
    help = "Importa una clase (salida/cNN/leccion.json) como lección en BORRADOR."

    def add_arguments(self, parser):
        parser.add_argument("carpeta", help="Carpeta salida/cNN del pipeline (con leccion.json)")
        parser.add_argument("--curso", default=CURSO_POR_DEFECTO["slug"], help="slug del curso")
        parser.add_argument("--modulo-titulo", default=None, help="título del módulo si hay que crearlo")
        parser.add_argument("--gratis", action="store_true", help="marcar como vista previa gratuita")

    @transaction.atomic
    def handle(self, *args, **opts):
        carpeta = Path(opts["carpeta"])
        manifiesto = carpeta / "leccion.json"
        if not manifiesto.exists():
            raise CommandError(f"No existe {manifiesto}. Ejecuta antes herramientas/montar.py.")
        m = json.loads(manifiesto.read_text(encoding="utf-8"))
        n = int(m["clase"])

        course = Course.objects.filter(slug=opts["curso"]).first()
        if course is None:
            track, _ = Track.objects.get_or_create(
                slug="curso-completo", defaults={"name": "Curso completo", "order": 0}
            )
            datos = {**CURSO_POR_DEFECTO, "slug": opts["curso"]}
            course = Course.objects.create(track=track, is_published=False, **datos)
            self.stdout.write(f"Curso creado (no publicado): {course.title}")

        num_mod = int(m.get("modulo") or 1)
        titulo_mod = opts["modulo_titulo"] or m.get("modulo_titulo") or f"Módulo {num_mod}"
        module, creado = Module.objects.get_or_create(
            course=course, order=num_mod, defaults={"title": f"Módulo {num_mod} · {titulo_mod}"}
        )
        if creado:
            self.stdout.write(f"Módulo creado: {module.title}")

        clave = f"CA-c{n:02d}"
        lesson = Lesson.objects.filter(source_key=clave).first() or Lesson(source_key=clave)
        lesson.module = module
        lesson.title = f"Clase {n}: {m['titulo']}"
        lesson.slug = m["slug"]
        lesson.description = m.get("descripcion", "")
        lesson.duration_minutes = int(m.get("duracion_min") or 0)
        lesson.order = n
        lesson.is_draft = True
        lesson.is_free_preview = bool(opts["gratis"])
        lesson.save()

        def adjuntar(campo, nombre):
            if not nombre:
                return
            ruta = carpeta / nombre
            if not ruta.exists():
                raise CommandError(f"Falta el archivo {ruta}")
            f = getattr(lesson, campo)
            if f:
                f.delete(save=False)
            with ruta.open("rb") as fh:
                f.save(ruta.name, File(fh), save=False)

        adjuntar("video_file", m.get("video"))
        adjuntar("subtitles_file", m.get("subtitulos_vtt"))
        adjuntar("thumbnail", m.get("miniatura"))
        lesson.save()

        for a in lesson.attachments.all():
            a.file.delete(save=False)
            a.delete()
        for i, a in enumerate(m.get("adjuntos", [])):
            ruta = carpeta / a["archivo"]
            if not ruta.exists():
                raise CommandError(f"Falta el archivo {ruta}")
            with ruta.open("rb") as fh:
                LessonAttachment.objects.create(lesson=lesson, title=a["titulo"], order=i, file=File(fh, name=ruta.name))

        lesson.quiz_questions.all().delete()
        quiz = m.get("quiz") or {}
        for i, q in enumerate(quiz.get("preguntas", [])):
            pregunta = QuizQuestion.objects.create(
                lesson=lesson, text=q["enunciado"], explanation=q.get("retroalimentacion", ""), order=i
            )
            correcta = q.get("correcta")
            for j, texto in enumerate(q.get("opciones", [])):
                QuizChoice.objects.create(question=pregunta, text=texto, is_correct=(j == correcta), order=j)

        self.stdout.write(self.style.SUCCESS(
            f"Lección importada como BORRADOR: {lesson.title} en {lesson.get_absolute_url()}"
        ))
