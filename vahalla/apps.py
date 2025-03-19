from django.apps import AppConfig

class VahallaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vahalla'

    def ready(self):
        import vahalla.signals
