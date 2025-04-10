from flask import Flask, Response, request, render_template_string
from datetime import date, datetime, timedelta
from icalendar import Calendar, Event

app = Flask(__name__)

def generate_ics(year):
    """
    Generate an ICS file for the provided year.
    
    For each month, the function finds:
    - The first Wednesday (by checking the first 7 days).
    - The following Thursday (the day after the first Wednesday).
    
    Both events are set for 08:00 to 12:00 and share the title "DONT PARK on the street".
    """
    cal = Calendar()
    cal.add('prodid', '-//DONT PARK on the street Calendar//example.com//')
    cal.add('version', '2.0')
    
    for month in range(1, 13):
        first_day = date(year, month, 1)
        # Find the first Wednesday in the first 7 days of the month.
        for i in range(7):
            check_date = first_day + timedelta(days=i)
            if check_date.weekday() == 2:  # Wednesday (0=Monday, 2=Wednesday)
                first_wed = check_date
                break
        first_thu = first_wed + timedelta(days=1)
        
        # Create two events: one for the first Wednesday and one for the following Thursday.
        for event_date in [first_wed, first_thu]:
            event = Event()
            event.add('summary', 'DONT PARK on the street')
            # Combine date with start time 08:00 and end time 12:00.
            event_start = datetime.combine(event_date, datetime.strptime("08:00", "%H:%M").time())
            event_end = datetime.combine(event_date, datetime.strptime("12:00", "%H:%M").time())
            event.add('dtstart', event_start)
            event.add('dtend', event_end)
            event.add('dtstamp', datetime.now())
            # UID should be unique; using a combination of year, month, day and a domain.
            event.add('uid', f"{year}-{month}-{event_date.day}@dontpark")
            cal.add_component(event)
    
    return cal.to_ical()

@app.route('/ics')
def ics():
    """
    Endpoint to download the ICS file.
    
    You can pass a query parameter "year" to specify the calendar year (default is the current year).
    For example: /ics?year=2025
    """
    year_param = request.args.get('year')
    year = int(year_param) if year_param and year_param.isdigit() else datetime.now().year
    ics_file = generate_ics(year)
    return Response(ics_file,
                    mimetype='text/calendar',
                    headers={'Content-Disposition': 'attachment; filename=calendar.ics'})

@app.route('/')
def index():
    """
    Basic homepage with a link to download the ICS file.
    """
    html_template = """
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <title>DONT PARK on the street Calendar</title>
      </head>
      <body>
        <h1>DONT PARK on the street Calendar</h1>
        <p>
          To subscribe to your calendar, download the ICS file by clicking
          <a href="/ics">here</a>.
        </p>
        <p>You can add <code>?year=2025</code> to the URL to generate a calendar for a specific year.</p>
      </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    # For local development use; when deploying on Render, use "gunicorn app:app" instead.
    app.run(debug=True)
