from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name="home"),
    path('', views.home, name="home"),
    path('user_profile', views.user_profile, name="user-profile"),
    path('update_user_profile', views.update_user_profile, name="update-user-profile"),
    path('event_list', views.all_events, name="event_list"),
    path('add_venue', views.add_venue, name="add-venue"),
    path('venues_list', views.list_venues, name="list-venues"),
    path('show_venue/<venue_id>', views.show_venue, name="show-venue"),
    path('search_venues', views.search_venues, name="search-venues"),
    path('update_venue/<venue_id>', views.update_venue, name="update-venue"),
    path('update_event/<event_id>', views.update_event, name="update-event"),
    path('add_event', views.add_event, name="add-event"),
    path('delete_event/<event_id>', views.delete_event, name="delete-event"),
    path('delete_venue/<venue_id>', views.delete_venue, name="delete-venue"),
    path('venue_text/', views.venue_text, name="venue-text"),
    path('venue_csv', views.venue_csv, name="venue-csv"),
    path('venue_pdf', views.venue_pdf, name="venue-pdf"),
    path('my_events', views.my_events, name="my-events"),
    path('search_events', views.search_events, name="search-events"),
    path('venue_events/<venue_id>', views.venue_events, name="venue-events"),
]
