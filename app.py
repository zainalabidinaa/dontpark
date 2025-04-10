from flask import Flask, Response, request
from datetime import date, datetime, timedelta
import pytz
from icalendar import Calendar, Event

app = Flask(__name__)

def generate_ics_range(start_year, end_year):
    """
    Generate an ICS file with events for every month from start_year to end_year (inclusive).

    For each month, the function calculates:
      - The first Wednesday (by checking the first 7 days).
      - The following Thursday (the day after the first Wednesday).

    Both events are set from 08:00 to 12:00 and labeled "DONT PARK on the street".
    Timezone information is added using pytz (default: Europe/Stockholm).
    """
    cal = Calendar()
    cal.add('prodid', '-//DONT PARK on the street Calendar//example.com//')
    cal.add('version', '2.0')

    # Set your desired timezone (modify if needed)
    tz = pytz.timezone('Europe/Stockholm')

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            first_day = date(year, month, 1)
            # Find the first Wednesday (weekday() == 2) in the first 7 days
            for i in range(7):
                check_date = first_day + timedelta(days=i)
                if check_date.weekday() == 2:
                    first_wed = check_date
                    break
            # The Thursday is the day immediately after the first Wednesday
            first_thu = first_wed + timedelta(days=1)

            # Create events for both days
            for event_date in [first_wed, first_thu]:
                event = Event()
                event.add('summary', 'DONT PARK on the street')
                dt_start = tz.localize(datetime.combine(event_date, datetime.strptime("08:00", "%H:%M").time()))
                dt_end = tz.localize(datetime.combine(event_date, datetime.strptime("12:00", "%H:%M").time()))
                event.add('dtstart', dt_start)
                event.add('dtend', dt_end)
                event.add('dtstamp', datetime.now(tz))
                event.add('uid', f"{year}-{month}-{event_date.day}@dontpark")
                cal.add_component(event)

    return cal.to_ical()

@app.route('/')
def ics():
    """
    The root endpoint now returns the ICS file directly.
    
    It accepts optional query parameters:
      - start_year: Beginning of the year range.
      - end_year: End of the year range.
    
    By default (if no parameters are provided), the ICS file will include events from
    the current year to the current year + 10.
    
    Now your calendar subscription URL will simply be:
      https://your-app.onrender.com/
    """
    current_year = datetime.now().year
    start_year_param = request.args.get('start_year')
    end_year_param = request.args.get('end_year')

    if start_year_param and end_year_param and start_year_param.isdigit() and end_year_param.isdigit():
        start_year = int(start_year_param)
        end_year = int(end_year_param)
    else:
        start_year = current_year
        end_year = current_year + 10

    ics_file = generate_ics_range(start_year, end_year)
    return Response(ics_file,
                    mimetype='text/calendar',
                    headers={'Content-Disposition': 'attachment; filename=calendar.ics'})

if __name__ == '__main__':
    # Use this for local development.
    # In production (for example, on Render), use a server like gunicorn (e.g. "gunicorn app:app").
    app.run(debug=True)
