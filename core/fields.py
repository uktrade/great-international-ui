from directory_components.forms.fields import DirectoryComponentsFieldMixin

from django import forms


class IntegerField(DirectoryComponentsFieldMixin, forms.IntegerField):
    pass
