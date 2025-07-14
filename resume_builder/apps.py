from django.apps import AppConfig


class ResumeBuilderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resume_builder'
    def ready(self):
        import resume_builder.signals  # 👈 This line connects the signals