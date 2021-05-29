from django.apps import AppConfig

class CovidConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userdb'

    def ready(self):
        from emailer import covidNotifier
        covidNotifier.schedule_Notifier();

