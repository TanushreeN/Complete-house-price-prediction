from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    AREA_UNITS = [('sq_meter', 'Square Meters'), ('sq_feet', 'Square Feet')]

    area_unit = forms.ChoiceField(choices=AREA_UNITS, required=True, label="Area Unit")  # Add dropdown

    predictedprice = forms.IntegerField(widget=forms.HiddenInput,initial=1)
    class Meta:
        model = Property
        fields = ['area', 'bedrooms', 'bathrooms','state', 'city', 'zipcode','stories', 'mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'parking', 'prefarea', 'furnishingstatus', 'costpersqunit', 'final_estimation']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.predictedprice = self.cleaned_data["predictedprice"]
        if commit:
            instance.save()
        return instance