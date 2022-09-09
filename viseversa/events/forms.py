from django import forms
from django.forms import ModelForm
from .models import Venue, Event

# Create a venue form
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        # fields = "__all__" Include all fields in the form
        fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email_address')
        labels = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_address': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':"Venue\'s name"}),
            'address':forms.TextInput(attrs={'class':'form-control', 'placeholder':"Venue\'s address"}),
            'zip_code':forms.TextInput(attrs={'class':'form-control', 'placeholder':"Zip_code"}),
            'phone':forms.TextInput(attrs={'class':'form-control', 'placeholder':"Venue\'s telephone number"}),
            'web':forms.TextInput(attrs={'class':'form-control', 'placeholder':"Web-site"}),
            'email_address':forms.EmailInput(attrs={'class':'form-control', 'placeholder':"Email address"}),
        }

# admin form
class EventFormAdmin(ModelForm):
    class Meta:
        model=Event
        fields=('name', 'event_date', 'venue', 'manager', 'attendees', 'description',)
        labels = {
            'name': '',
            'event_date': '',
            'venue': 'Venue:',
            'manager': 'Manager:',
            'attendees': 'Attendees:',
            'description': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Event\'s name"}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Event\'s date"}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': "Venue"}),
            'manager': forms.Select(attrs={'class': 'form-select', 'placeholder': "Manager"}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': "Attendees"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Description"}),
        }



class EventForm(ModelForm):
    class Meta:
        model=Event
        fields=('name', 'event_date', 'venue', 'attendees', 'description',)
        labels = {
            'name': '',
            'event_date': '',
            'venue': 'Venue:',
            'attendees': 'Attendees:',
            'description': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Event\'s name"}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Event\'s date"}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': "Venue"}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': "Attendees"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Description"}),
        }