from django import forms

from filmsapp.models import Films, FilmsCategory


class FilmEditForm(forms.ModelForm):
    class Meta:
        model = Films
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FilmEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CatEditForm(forms.ModelForm):
    class Meta:
        model = FilmsCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CatEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
