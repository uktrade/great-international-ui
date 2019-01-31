from django.conf import settings


class LanguageSwitcherEnabledMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            language_switcher={
                'show': True,
                'available_languages': settings.LANGUAGES,
                'language_available': True
            },
            **kwargs)
        return context
