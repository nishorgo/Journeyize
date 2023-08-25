from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta

class RegionForm(forms.Form):
    region_name = forms.CharField(label='City Name', max_length=100)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'id': 'start-date', 'min': date.today(), 'placeholder': 'Start Date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'id': 'end-date', 'placeholder': 'End Date'}))

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if end_date - start_date > timedelta(days=10):
            raise ValidationError("The duration shouldn't be more than 10 days.")
        elif end_date - start_date < timedelta(days=0):
            raise ValidationError("End date shouldn't be before start date.")



class PlacesForm(forms.Form):
    selected_places = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[])

    def __init__(self, *args, **kwargs):
        places_list = kwargs.pop('places_list', None)
        super(PlacesForm, self).__init__(*args, **kwargs)
        self.fields['selected_places'].choices = [(place, place) for place in places_list]
