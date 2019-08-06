from django.utils import translation


class LocalisedURLsMixin:
    @property
    def localised_urls(self):
        localised = []
        requested_language = translation.get_language()
        url = self.request.build_absolute_uri().split('?')[0]

        for code, language in self.available_languages:
            if code == requested_language:
                continue
            else:
                localised_page = url + f'?lang={code}'
                localised.append([localised_page, code])

        return localised

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            localised_urls=self.localised_urls,
            *args, **kwargs)
