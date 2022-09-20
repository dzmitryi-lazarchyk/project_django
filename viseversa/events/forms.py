from django import forms
from django.forms import ModelForm, Form
from .models import Venue, Event, MyUser
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from tempus_dominus.widgets import DateTimePicker

# Create a venue form
class UserForm(forms.Form):
    fields = ('username', 'first_name', 'last_name',
              'email',
              'ava', 'description')
    ava = forms.ImageField()
    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class':'form-conrol', 'placeholder':'Useername'}))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class':'form-conrol', 'placeholder':'First name'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class':'form-conrol', 'placeholder':'Last name'}))
    email = forms.CharField(max_length=60,widget=forms.EmailInput(
        attrs={'class':'form-conrol', 'placeholder':'Email address'}))
    description = forms.CharField(max_length=300,widget=forms.Textarea(
        attrs={'class':'form-conrol', 'placeholder':'Email address'}))


class VenueForm(ModelForm):

    class Meta:
        model = Venue
        # fields = "__all__" Include all fields in the form
        fields = ('name', 'address', 'zip_code',
                  'phone', 'web', 'email_address',
                  'venue_image')
        labels = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_address': '',
            'venue_image': '',
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

    def __init__(self, user, *args, **kwargs):
        super(EventFormAdmin, self).__init__(*args, **kwargs)
        users = get_user_model().objects.exclude(username=user.username)
        self.fields['attendees'].choices = ([(user.id, user) for user in users]

        )
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
            'event_date': DateTimePicker(options={'useCurrent': True, 'collapse': False,},
                                         attrs={'append': 'fa fa-calendar', 'icon_toggle': True,}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': "Venue"}),
            'manager': forms.Select(attrs={'class': 'form-select', 'placeholder': "Manager"}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': "Attendees"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Description", }),
        }



class EventForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        users = get_user_model().objects.exclude(username=user.username)
        self.fields['attendees'].choices = ([(user.id, user) for user in users]

        )
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
            'event_date': DateTimePicker(options={'useCurrent': True, 'collapse': False,},
                                         attrs={'append': 'fa fa-calendar', 'icon_toggle': True,}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': "Venue"}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': "Attendees"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Description"}),
        }

