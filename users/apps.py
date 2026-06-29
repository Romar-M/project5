from django.apps import AppConfig


class UsersConfig(AppConfig):
    def ready(self):
        import users.signals
    name = "users"
