from directory_components.forms.fields import DirectoryComponentsFieldMixin
from captcha.fields import ReCaptchaField


class DirectoryComponentsRecaptchaField(DirectoryComponentsFieldMixin, ReCaptchaField):
    pass
