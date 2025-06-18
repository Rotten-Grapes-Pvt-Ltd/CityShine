from django import forms
from django.contrib.gis.forms import PointField
from django.contrib.gis.geos import Point
from .models import Issue

class IssueForm(forms.ModelForm):
    latitude = forms.FloatField(
        min_value=-90,
        max_value=90,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    longitude = forms.FloatField(
        min_value=-180,
        max_value=180,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    
    class Meta:
        model = Issue
        fields = ['issue_type', 'title', 'description', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'issue_type': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If instance is provided and has a location, populate lat/lng fields
        if self.instance.pk and self.instance.location:
            self.fields['latitude'].initial = self.instance.location.y
            self.fields['longitude'].initial = self.instance.location.x
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Get latitude and longitude from the form
        latitude = self.cleaned_data.get('latitude')
        longitude = self.cleaned_data.get('longitude')
        
        # Create a Point object and assign it to the location field
        if latitude and longitude:
            instance.location = Point(longitude, latitude, srid=4326)
        
        if commit:
            instance.save()
        
        return instance

class UpdateIssueStatusForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'})
        }