from django import forms

class RegionForm(forms.Form):
    region_name = forms.CharField(label='City Name', max_length=100)


class PlacesForm(forms.Form):
    region_name = forms.CharField(widget=forms.HiddenInput())
    selected_places = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[])

    def __init__(self, *args, **kwargs):
        places_list = kwargs.pop('places_list', None)
        super(PlacesForm, self).__init__(*args, **kwargs)
        self.fields['selected_places'].choices = [(place, place) for place in places_list]


class FoodsForm(forms.Form):
    region_name = forms.CharField(widget=forms.HiddenInput())
    selected_places = forms.CharField(widget=forms.HiddenInput())
    selected_foods = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[])

    def __init__(self, *args, **kwargs):
        foods_list = kwargs.pop('foods_list', None)
        super(FoodsForm, self).__init__(*args, **kwargs)
        self.fields['selected_foods'].choices = [(food, food) for food in foods_list]
