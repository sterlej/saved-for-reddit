from django.apps import AppConfig


class StorageConfig(AppConfig):
    name = 'storage'


class ProfileConfig(AppConfig):
    name = "storage"
    verbose_name = 'User Profiles'

    def ready(self):
        from . import signals
