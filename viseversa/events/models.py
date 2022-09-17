from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import date
from django.db.models import Q


class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15, blank=True)
    phone = models.CharField('Contact Phone', max_length=25)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('Email Address', blank=True)
    owner = models.IntegerField("Venue Owner", blank=False, default=1)
    venue_image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name


class MyclubUser(models.Model):
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300, blank=True)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

user_model = get_user_model()
class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    # venue = models.CharField(max_length=120)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='manager')
    description = models.TextField(blank=True)
    attendees=models.ManyToManyField(user_model, blank=False)
    # attendees=models.ManyToManyField(user_model, blank=True,
    #                                  limit_choices_to=Q(username__startswith='admin'),)

    def __str__(self):
        return self.name

    def caps(self):
        return str(self.name).capitalize()

    @property
    def days_till(self):
        today= date.today()
        days_till=self.event_date.date()-today
        return days_till
