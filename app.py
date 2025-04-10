from flask import Flask, render_template_string, request
from datetime import datetime, date, timedelta

app = Flask(__name__)

def get_first_wednesday_and_thursday(year):
    """
    For each month in the given year, find the first Wednesday and the Thursday following it.
    
    Explanation:
    - We loop over each month (from 1 to 12).
    - For each month, we start at the 1st and iterate through the first 7 days.
      This ensures we catch the first occurrence of a Wednesday (weekday() == 2, since Monday is 0).
    - Once the first Wednesday is found, the immediate next day (Wednesday + 1 day) is taken as the Thursday.
    - Each event uses the time slot "08:00–12:00" and the title "DONT PARK on the street".
    """
    events = []
    for month in range(1, 13):
        # Define the first day of the month.
        first_day = date(year, month, 1)
        # Find the first Wednesday in the first 7 days.
        for i in range(7):
            current_day = first_day + timedelta(days=i)
            if current_day.weekday() == 2:  # Wednesday (0=Monday, so 2=Wednesday)
                first_wed = current_day
                break
        # The corresponding Thursday is the day after the first Wednesday.
        first_thu = first_wed + timedelta(days=1)
        
        # Save the events information in a dictionary.
        events.append({
            'month': first_day.strftime("%B"),  # Full month name
            'wednesday': first_wed.strftime("%A %d-%m-%Y"),  # e.g., "Wednesday 04-04-2024"
            'thursday': first_thu.strftime("%A %d-%m-%Y"),   # e.g., "Thursday 05-04-2024"
            'time': "08:00-12:00",
            'title': "DONT PARK on the street"
        })
    return events

@app.route('/')
def index():
    """
    This route renders an HTML page that lists all months with their associated events.
    
    You can pass an optional query parameter 'year' to choose the calendar year.
    For example: http://your-app-url/?year=2025 
    """
    # Get the 'year' from query params, or default to the current year.
    year_param = request.args.get('year')
    year = int(year_param) if year_param and year_param.isdigit() else datetime.now().year
    
    events = get_first_wednesday_and_thursday(year)
    
    # A simple HTML template using render_template_string.
    html_template = """
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <title>DONT PARK on the street Calendar</title>
      </head>
      <body>
        <h1>DONT PARK on the street Calendar for {{ year }}</h1>
        <table border="1" cellspacing="0" cellpadding="8">
          <tr>
            <th>Month</th>
            <th>First Wednesday</th>
            <th>First Thursday</th>
            <th>Time</th>
            <th>Title</th>
          </tr>
          {% for event in events %}
          <tr>
            <td>{{ event.month }}</td>
            <td>{{ event.wednesday }}</td>
            <td>{{ event.thursday }}</td>
            <td>{{ event.time }}</td>
            <td>{{ event.title }}</td>
          </tr>
          {% endfor %}
        </table>
      </body>
    </html>
    """
    return render_template_string(html_template, events=events, year=year)

if __name__ == '__main__':
    # When running locally, start Flask's development server.
    # For deployment on Render, ensure your startup command runs "gunicorn app:app" (if the file is named app.py).
    app.run(debug=True)
