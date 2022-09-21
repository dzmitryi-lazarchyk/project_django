import calendar

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from calendar import HTMLCalendar
from django.utils import timezone
from .models import Event, Venue, MyUser
from .forms import VenueForm, EventForm, EventFormAdmin, MyUserForm
from django.http import HttpResponse
import csv
from django.contrib import messages
from django.contrib.auth.models import User
from django.core import exceptions
from django.contrib.auth import get_user_model

# Import PDF Stuff
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Import Pagination Stuff
from django.core.paginator import Paginator

# ddecorator
from django.contrib.auth.models import User

def authenticated(f):
    def wrapper(*args, **kwargs):
        if args[0].user.is_authenticated:
            res = f(*args, **kwargs)
            return res
        else:
            return redirect('login')

    return wrapper

def user_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    my_user = MyUser.objects.get(user=user)
    return render(request, 'events/user_profile.html', {'info':my_user.get_info(),
                                                        'my_user':my_user,})

def update_user_profile(request):
    submitted=False
    if request.method == "POST":
        my_user = MyUser.objects.get(user=request.user)
        user=request.user
        form=MyUserForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()

            my_user.ava=request.FILES.get('ava')
            my_user.description=request.POST.get('description')
            my_user.save()
            return redirect('home')
    else:
        user = request.user
        my_user = MyUser.objects.get(user=user)
        form = MyUserForm(initial={"username":user, "first_name":user.first_name,
                                   "last_name":user.last_name, "email":user.email,
                                   "description":my_user.description,
                                   "ava":my_user.ava})
        if 'submitted' in request.GET:
            submitted=True
    return render(request, 'events/update_user_profile.html', {'form': form, 'submitted': submitted})

# Generate text file
@authenticated
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    # Designate the model
    venues = Venue.objects.all()
    # Create blank list
    lines = []
    no_zip = 'No zip-code'
    # Loop through and uotput
    for venue in venues:
        lines.append(f'{venue.name}:\n'
                     f'  {venue.address}\n'
                     f'  {venue.zip_code if venue.zip_code != "None" else no_zip}\n'
                     f'  {venue.web}\n'
                     f'  {venue.email_address}\n\n')
    # lines=["This is line 1\n",
    #        "This is line 2\n",
    #        "This is line 3\n"]
    #     Write to text file
    response.writelines(lines)
    return response

@authenticated
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    # Create a csv writer
    writer = csv.writer(response)
    # Designate the model
    venues = Venue.objects.all()
    # add column headings to csv file
    writer.writerow(['Venue name', 'Address', 'Zip Code',
                     'Web Address', 'Email'])
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code,
                         venue.web, venue.email_address])
        # writer.writerow(getattr(venue, field.name))

    return response


# Generate a PDF File Venue List
# pip install reportlab
@authenticated
def venue_pdf(request):
    # Create bytestream buffer
    buf = io.BytesIO()
    # Create canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    # Add some lines of text
    # lines=[
    #     "This is line 1",
    #     "This is line 2",
    #     "This is line 3",
    # ]
    venues = Venue.objects.all()
    lines = []
    no_zip = 'No zip-code'
    for venue in venues:
        lines.append(venue.name)
        lines.append('\t' + venue.address)
        lines.append('\t' + venue.zip_code if venue.zip_code != "None" else '\t' + no_zip)
        lines.append('\t' + venue.web)
        lines.append('\t' + venue.email_address)
        lines.append('')
    for line in lines:
        textob.textLine(line)
    # finishup
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='Venue.pdf')

@authenticated
def home(request):
    name = request.user
    # # Convert month from name to number
    # month = month.capitalize()
    # month_number = int(list(calendar.month_name).index(month))
    #
    # # Create a calendar
    # cal = HTMLCalendar().formatmonth(year, month_number)
    #
    # # Get current year
    # now = datetime.now()
    # current_year = now.year
    #
    # # Get current time
    # time = now.strftime("%H:%M")
    #
    # return render(request, 'events/home.html', {
    #     "name": name,
    #     "year": year,
    #     "month": month,
    #     "month_number": month_number,
    #     "cal": cal,
    #     "current_year": current_year,
    #     "time": time,
    # })
    events = Event.objects.all().order_by('event_date', 'name')
    event_list=[]
    for event in events:
        if event.event_date>timezone.now():
            event_list.append(event)

    context= {'name':name}
    if event_list:
        try:
            context['event_list'] = event_list[:3]
        except IndexError:
            context['event_list'] = event_list
    return render(request, 'events/home.html', context)
@authenticated
def all_events(request):
    event_list = Event.objects.all().order_by('event_date', 'name')
    # Set up Pagination
    p = Paginator(event_list, 3)
    page = request.GET.get('page')
    events = p.get_page(page)
    num_pages = events.paginator.num_pages
    if num_pages > 4:
        model = {1: [1, 2, 3],
                 2: [1, 2, 3],
                 num_pages - 1: [num_pages - 2, num_pages - 1, num_pages],
                 num_pages: [num_pages - 2, num_pages - 1, num_pages]}. \
            get(events.number,
                [0, events.number - 1, events.number, events.number + 1, 0])
    else:
        model = False
    return render(request, 'events/event_list.html', {
        'event_list': event_list,
        'events': events,
        'model': model
    })

@authenticated
def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    form = VenueForm
    return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})

@authenticated
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')

@authenticated
def list_venues(request):
    # Order by random
    # venue_list = Venue.objects.all().order_by('?')
    venue_list = Venue.objects.all().order_by('name')

    # Set up Pagination
    p = Paginator(venue_list, 1)
    page = request.GET.get('page')
    venues = p.get_page(page)
    num_pages = venues.paginator.num_pages
    if num_pages > 4:
        model = {1: [1, 2, 3],
                 2: [1, 2, 3],
                 num_pages - 1: [num_pages - 2, num_pages - 1, num_pages],
                 num_pages: [num_pages - 2, num_pages - 1, num_pages]}. \
            get(venues.number,
                [0, venues.number - 1, venues.number, venues.number + 1, 0])
    else:
        model = False

    return render(request, 'events/venues.html', {
        'venue_list': venue_list,
        'venues': venues,
        'model': model
    })

@authenticated
def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    try:
        venue_owner=User.objects.get(pk=venue.owner)
    except exceptions.ObjectDoesNotExist:
        venue_owner='No owner'
    return render(request, 'events/show_venue.html', {
        'venue': venue,
        'venue_owner': venue_owner,
    })

@authenticated
def search_venues(request):
    if request.method == "POST":
        searched = request.POST.get("searched", False)
        venues = Venue.objects.filter(name__contains=searched)
        events = Event.objects.filter(name__contains=searched)
        return render(request, 'events/search_venues.html',
                      {'searched': searched,
                       'venues': venues,
                       'events': events,
                       })
    else:
        return render(request, 'events/search_venues.html', {})

@authenticated
def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    return render(request, 'events/update_venue.html', {
        'venue': venue,
        'form': form,
    })

@authenticated
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if event.manager == request.user:
        not_manager = False
    else:
        not_manager = True
    form = EventForm(request.user, data=request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, 'events/update_event.html', {
        'event': event,
        'form': form,
        'not_manager':not_manager,
    })


@authenticated
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if event.manager==request.user:
        event.delete()
        messages.success(request, ("Event deleted successfully!"))
        return redirect('event_list')
    else:
        messages.success(request, ("You aren't authorized to delete this event."))
        return redirect('event_list')

@authenticated
def add_event(request):
    submitted = False
    if request.method == "POST":
        print(request.POST)
        if request.user.is_superuser:
            form = EventFormAdmin(request.user, data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
            else:
                print(form.errors)
        else:
            form = EventForm(request.user, data=request.POST)
            if form.is_valid():
                print('yes')
                event = form.save(commit=False)
                event.manager = request.user
                print(event.manager)
                form.save()
                # form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        if request.user.is_superuser:
            form = EventFormAdmin(request.user)
        else:
            form = EventForm(request.user)
        if 'submitted' in request.GET:
            submitted = True
    if request.user.is_superuser:
        form = EventFormAdmin(request.user)
    else:
        form = EventForm(request.user)
    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})

@authenticated
def my_events(request):

    events_manager=Event.objects.filter(manager=request.user.id)
    events_attendees=Event.objects.filter(attendees=request.user.id)
    return render(request,
                  'events/my_events.html', {
                  'events_manager':events_manager,
                  'events_attendees':events_attendees,
                  })

def search_events(request):
    if request.method == "POST":
        searched = request.POST.get("searched", False)
        events = Event.objects.filter(name__contains=searched)
        return render(request, 'events/search_events.html',
                      {'searched': searched,
                       'events': events})
    else:
        return render(request, 'events/search_events.html', {})

def venue_events(request, venue_id):
    events = Event.objects.filter(venue=venue_id)
    venue=Venue.objects.get(pk=venue_id)
    return render(request, 'events/venue_events.html', {
        'events': events,
        'venue': venue,
    })