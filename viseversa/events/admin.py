from django.contrib import admin
from .models import Venue, Event, MyUser

# admin.site.register(Venue)
# admin.site.unregister(MyclubUser)
# admin.site.register(Event)


@admin.register(Venue) # Modify admin area 1st method
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    ordering = ('name', )
    search_fields = ('name', 'address')
    search_help_text = True

# admin.site.register(Venue, VenueAdmin) Delete 8th string # Modify admin area 2nd method

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'manager', 'attendees','description')
    list_display = ('name', 'venue', 'event_date')
    list_filter = ('event_date', 'venue')
    ordering = ('event_date', )
