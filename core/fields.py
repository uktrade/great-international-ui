from directory_components.fields import DirectoryComponentsFieldMixin

from django import forms


class IntegerField(DirectoryComponentsFieldMixin, forms.IntegerField):
    pass
