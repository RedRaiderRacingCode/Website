'''
author: Carson Spaniel
date: 9/9/23
'''

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from datetime import datetime

def emailMessage(name, email, subject, message):
    '''
    Used to take the inputs and send an email to our email.
        - currently using 'redraiderracingcode@outlook.com' for testing.
    '''
    message = formatMessage(name,email,message)
    try:
        send_mail(
            subject,
            message,
            'redraiderracing@website.admin',
            ['redraiderracingcode@outlook.com'],
            fail_silently=False,
        )
        return HttpResponse('Success.')
    except BadHeaderError:
        # Handle a BadHeaderError (e.g., invalid subject)
        return HttpResponse('Invalid header found.')
    except Exception as e:
        # Handle other exceptions (e.g., SMTP errors, connection issues)
        return HttpResponse(f'An error occurred: {str(e)}')

def formatMessage(name, email, message):
    '''
    Used to format the message how ever you want.
    '''
    day_of_week = datetime.now().strftime('%A') # Full day name (e.g., "Monday")
    date = datetime.now().strftime('%m/%d/%Y') # In the format MM/DD/YYYY

    hour = datetime.now().hour
    minute = datetime.now().minute
    if hour > 12:
        hour -= 12
        dayTime = 'PM'
    elif hour == 12:
        dayTime = 'PM'
    else:
        dayTime = 'AM'

    if minute < 10:
        minute = f'0{minute}'

    email_link = f'<a href="mailto:{email}">{email}</a>' # Makes a clickable link in the email
    
    message = f'This message is from {name} on {day_of_week} {date} at {hour}:{minute} {dayTime}:\n\n\n{message}\n\n\nTo respond to them, email them back at {email_link}.'
    print(message)
    return message 

# formatMessage("Carson Spaniel","carsonspaniel@gmail.com","I would love to join the team. How can I start getting involved? \nThank you,\nCarson Spaniel")