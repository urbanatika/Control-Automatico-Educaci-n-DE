from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.courses.models import Course, Lesson, Module, Track

CURRICULUM = [
    {
        "name": "Fundamentos de Control Lineal",
        "icon": "📈",
        "description": "Modelado, función de transferencia, respuesta transitoria y estabilidad de sistemas lineales.",
        "course": {
            "title": "Introducción al Control Lineal",
            "summary": "Los cimientos de todo sistema de control: modelado, respuesta en el tiempo y estabilidad.",
            "description": (
                "Curso introductorio al control lineal: representación en espacio de estados y función "
                "de transferencia, análisis de respuesta transitoria y en régimen permanente, criterios "
                "de estabilidad (Routh-Hurwitz, lugar de las raíces) y diseño de controladores PID clásicos."
            ),
            "level": Course.Level.BASICO,
            "modules": [
                {
                    "title": "Modelado de sistemas",
                    "lessons": [
                        ("Introducción al curso y al control automático", 12, True),
                        ("Función de transferencia y espacio de estados", 22, False),
                    ],
                },
                {
                    "title": "Análisis de estabilidad",
                    "lessons": [
                        ("Criterio de Routh-Hurwitz", 18, False),
                        ("Lugar geométrico de las raíces", 25, False),
                    ],
                },
            ],
        },
    },
    {
        "name": "Control No Lineal",
        "icon": "🌀",
        "description": "Fenómenos no lineales, análisis en el plano de fase y métodos de Lyapunov.",
        "course": {
            "title": "Fundamentos de Control No Lineal",
            "summary": "Cuando el mundo real deja de comportarse en línea recta: análisis y control de sistemas no lineales.",
            "description": (
                "Estudio de sistemas no lineales: puntos de equilibrio, plano de fase, ciclos límite, "
                "estabilidad de Lyapunov y una introducción al control por modos deslizantes."
            ),
            "level": Course.Level.AVANZADO,
            "modules": [
                {
                    "title": "Análisis de sistemas no lineales",
                    "lessons": [
                        ("Fenómenos no lineales: qué cambia respecto al caso lineal", 15, True),
                        ("Plano de fase y puntos de equilibrio", 20, False),
                    ],
                },
                {
                    "title": "Estabilidad y control",
                    "lessons": [
                        ("Método directo de Lyapunov", 24, False),
                        ("Introducción al control por modos deslizantes", 26, False),
                    ],
                },
            ],
        },
    },
    {
        "name": "Linealización de Sistemas",
        "icon": "📐",
        "description": "Técnicas para aproximar sistemas no lineales alrededor de un punto de operación.",
        "course": {
            "title": "Linealización de Sistemas Dinámicos",
            "summary": "Cómo aproximar un sistema no lineal a uno lineal para diseñar controladores clásicos.",
            "description": (
                "Linealización por series de Taylor alrededor de un punto de equilibrio, obtención del "
                "modelo en espacio de estados linealizado y validación de la aproximación mediante simulación."
            ),
            "level": Course.Level.INTERMEDIO,
            "modules": [
                {
                    "title": "Linealización alrededor de un punto de operación",
                    "lessons": [
                        ("Motivación: por qué linealizar", 10, True),
                        ("Linealización por series de Taylor", 20, False),
                    ],
                },
            ],
        },
    },
    {
        "name": "Técnicas y Estrategias Avanzadas de Control",
        "icon": "🧠",
        "description": "Control robusto, adaptativo, óptimo y predictivo (MPC).",
        "course": {
            "title": "Estrategias Avanzadas de Control",
            "summary": "Más allá del PID: control óptimo, robusto, adaptativo y predictivo basado en modelo.",
            "description": (
                "Panorama de estrategias avanzadas: control óptimo (LQR), control robusto, control "
                "adaptativo y control predictivo basado en modelo (MPC), con criterios para elegir "
                "la técnica adecuada según la aplicación."
            ),
            "level": Course.Level.AVANZADO,
            "modules": [
                {
                    "title": "Control óptimo y robusto",
                    "lessons": [
                        ("Panorama de estrategias avanzadas de control", 14, True),
                        ("Control óptimo: regulador lineal cuadrático (LQR)", 24, False),
                    ],
                },
                {
                    "title": "Control predictivo",
                    "lessons": [
                        ("Introducción al control predictivo basado en modelo (MPC)", 28, False),
                    ],
                },
            ],
        },
    },
    {
        "name": "Recorrido Histórico del Control Automático",
        "icon": "🕰️",
        "description": "La evolución de la teoría de control, de los reguladores mecánicos a la era digital.",
        "course": {
            "title": "Historia del Control Automático",
            "summary": "Del regulador centrífugo de Watt a los sistemas de control digital modernos.",
            "description": (
                "Un recorrido por los hitos que dieron forma al control automático: los primeros "
                "reguladores mecánicos, el desarrollo de la teoría de control clásica en el siglo XX, "
                "la llegada del control moderno en espacio de estados y la era del control digital y "
                "los sistemas embebidos."
            ),
            "level": Course.Level.BASICO,
            "modules": [
                {
                    "title": "De los reguladores mecánicos al control clásico",
                    "lessons": [
                        ("El regulador de Watt y los orígenes del control", 12, True),
                        ("El nacimiento de la teoría de control clásica", 18, False),
                    ],
                },
                {
                    "title": "Control moderno y digital",
                    "lessons": [
                        ("La era del espacio de estados y el control moderno", 16, False),
                        ("Control digital y sistemas embebidos", 15, False),
                    ],
                },
            ],
        },
    },
    {
        "name": "Herramientas de Control",
        "icon": "🛠️",
        "description": "Software y hardware para simular, diseñar e implementar sistemas de control.",
        "course": {
            "title": "Herramientas para el Diseño de Control",
            "summary": "MATLAB/Simulink, Python, PLCs y microcontroladores aplicados al control automático.",
            "description": (
                "Introducción práctica a las herramientas más usadas por ingenieros de control: "
                "MATLAB y Simulink para simulación y diseño, Python como alternativa de código abierto, "
                "y una introducción a PLCs y microcontroladores para implementación en tiempo real."
            ),
            "level": Course.Level.INTERMEDIO,
            "modules": [
                {
                    "title": "Simulación y diseño",
                    "lessons": [
                        ("MATLAB y Simulink para control", 20, True),
                        ("Python para control automático (python-control, NumPy)", 22, False),
                    ],
                },
                {
                    "title": "Implementación en tiempo real",
                    "lessons": [
                        ("Introducción a PLCs para control industrial", 18, False),
                        ("Microcontroladores y control embebido", 20, False),
                    ],
                },
            ],
        },
    },
    {
        "name": "Aplicaciones de Laboratorio e Industriales",
        "icon": "🏭",
        "description": "Casos reales de control aplicado en laboratorio y en procesos industriales.",
        "course": {
            "title": "Control Aplicado: Laboratorio e Industria",
            "summary": "Casos de estudio reales para llevar la teoría de control a sistemas físicos.",
            "description": (
                "Aplicación de los conceptos de control a casos reales de laboratorio (péndulo invertido, "
                "control de nivel y temperatura) y a procesos industriales típicos (control de procesos, "
                "lazos de control en plantas, buenas prácticas de sintonización)."
            ),
            "level": Course.Level.INTERMEDIO,
            "modules": [
                {
                    "title": "Montajes de laboratorio",
                    "lessons": [
                        ("Control de nivel y temperatura en laboratorio", 16, True),
                        ("Péndulo invertido: modelado y control", 24, False),
                    ],
                },
                {
                    "title": "Procesos industriales",
                    "lessons": [
                        ("Lazos de control en plantas industriales", 20, False),
                        ("Buenas prácticas de sintonización de controladores", 18, False),
                    ],
                },
            ],
        },
    },
]


class Command(BaseCommand):
    help = "Crea los ejes temáticos, cursos, módulos y lecciones de ejemplo del temario de control automático."

    def handle(self, *args, **options):
        for order, track_data in enumerate(CURRICULUM):
            track, _ = Track.objects.update_or_create(
                slug=slugify(track_data["name"]),
                defaults={
                    "name": track_data["name"],
                    "icon": track_data["icon"],
                    "description": track_data["description"],
                    "order": order,
                },
            )

            course_data = track_data["course"]
            course, _ = Course.objects.update_or_create(
                slug=slugify(course_data["title"]),
                defaults={
                    "track": track,
                    "title": course_data["title"],
                    "summary": course_data["summary"],
                    "description": course_data["description"],
                    "level": course_data["level"],
                    "order": 0,
                    "is_published": True,
                },
            )

            for module_order, module_data in enumerate(course_data["modules"]):
                module, _ = Module.objects.update_or_create(
                    course=course,
                    title=module_data["title"],
                    defaults={"order": module_order},
                )

                for lesson_order, (title, duration, is_free) in enumerate(module_data["lessons"]):
                    Lesson.objects.update_or_create(
                        module=module,
                        slug=slugify(title),
                        defaults={
                            "title": title,
                            "duration_minutes": duration,
                            "is_free_preview": is_free,
                            "order": lesson_order,
                        },
                    )

            self.stdout.write(self.style.SUCCESS(f"OK: {track.name} -> {course.title}"))

        self.stdout.write(self.style.SUCCESS("Temario de ejemplo creado correctamente."))
