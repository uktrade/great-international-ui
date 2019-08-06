from django.conf import settings


class LanguageSwitcherEnabledMixin:
    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            language_switcher={
                'show': True,
                'available_languages': settings.LANGUAGES,
                'language_available': True
            },
            *args, **kwargs)
