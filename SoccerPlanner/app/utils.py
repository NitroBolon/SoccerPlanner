from datetime import datetime, timedelta
from calendar import HTMLCalendar
import threading
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.middleware.csrf import get_token
from .models import Event


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, request=None):
        self.year = year
        self.month = month
        self.request = request
        super(Calendar, self).__init__()
        

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)
        d = ''
        for event in events_per_day:
            if self.request.user.is_authenticated:
                d += f'<li> {event.get_html_url} </li>'
            else:
                d += f'<li> {event.notes} </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr 
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
           	cal += f'{self.formatweek(week, events)}\n'
        return cal