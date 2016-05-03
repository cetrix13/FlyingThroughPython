import requests
import smtplib
# Use dictionary for emails 
def get_emails():
    emails = {} 
    try:
        email_file = open('emailer.txt', 'r')
        for line in email_file:
            # make use of Python tuple
            (email, name) = line.split(',')
            emails[email] = name.strip()
    except FileNotFoundError as err:
        print(err)
    return emails

def get_schedule():
    try:
        schedule_file = open('schedule.txt', 'r')
        schedule = schedule_file.read()
    except FileNotFoundError as err:
        print(err)
    return schedule 

def send_emails(emails, schedule, forecast):
    server = smtplib.SMTP('smtp.gmail.com', '587')
    # start encryption  
    server.starttls()
    # login
    password = input('Enter you password: ')
    from_email ='ivan.pertrushev@gmail.com'
    server.login(from_email, password)
    # send to entire email list
    for to_email, name in emails.items():
        message = 'Subject: Welcome to the Circus!\n'
        message += 'Hi ' + name + '!\n\n'
        message += forecast + '\n\n' 
        message += schedule + '\n\n' 
        server.sendmail(from_email, to_email, message) 
    server.quit()

def get_weather_forecast():
    url = "http://api.openweathermap.org/data/2.5/weather?q=London,uk&appid=4551cd5651e727189c90e0105997163c"
    weather_request = requests.get(url)
    weather_json = weather_request.json() 
    # Parsing JSON
    description = weather_json['weather'][0]['description']
    temp_min = weather_json['main']['temp_min']
    temp_max = weather_json['main']['temp_max']

    # Creating our forecast string
    forecast = 'The Circus forecast for today is '
    forecast += description + ' with a high of ' + str(int(temp_max))
    forecast += ' and a low of ' + str(int(temp_min)) + '.'
    return forecast

def main():
    emails = get_emails()
    print(emails)
    schedule = get_schedule()
    print(schedule)
    forecast = get_weather_forecast()
    send_emails(emails, schedule, forecast)
main()
