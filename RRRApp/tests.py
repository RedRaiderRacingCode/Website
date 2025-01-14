'''
author: Carson Spaniel
date: 10/17/23

To run the tests:
    py manage.py collectstatic # making sure the static is up to date
    py manage.py test RRRApp.tests
'''

from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from unittest.mock import patch

from django.core import mail
from RRRApp.functions.email import *
from RRRApp.functions.merch import merchMessageFormat
from .models import *
from .functions.carShowReg import insertRow

class EmailTestCase(TestCase):
    '''
    All tests associated with email.py
    '''

    def test_formatMessage_pass(self):
        '''
        This one should pass by using correct values.
        '''

        name = "John Doe"
        email = "john.doe@example.com"
        subject = "Test Subject."
        message = "This is a test message."

        # Call the function with the test input
        formatted_message = formatMessage(name, email, subject, message)

        # Check the expected output
        expected_message = f'This message is from {name} on {datetime.now().strftime("%A")}, {datetime.now().strftime("%m/%d/%Y")} at {datetime.now().strftime("%I")}:{datetime.now().strftime("%M")} {datetime.now().strftime("%p")}:\n\n\n{message}\n\n\nTo respond to them, email them back at <a href="mailto:{email}?subject=RE: {subject}">{email}</a>.'
        self.assertEqual(formatted_message, expected_message)

    def test_formatMessage_fail(self):
        '''
        This one should fail by using incorrect values.
        '''

        # Call the function with the test input
        formatted_message = formatMessage(None, None, None, None)

        # Check the expected output
        expected_message = False
        self.assertEqual(formatted_message, expected_message)


class IndexViewTestCase(TestCase):
    '''
    All tests associated with index in views.
    '''

    def test_index_view_GET(self):
        '''
        Testing to see if a GET request passes correctly and a template is returned.
        '''

        url = reverse('home') # More dynamic way to write 'home/'
        response = self.client.get(url)
        self.assertTrue(200 <= response.status_code < 400)

    def test_index_view_POST_email(self):
        '''
        Testing to see if a POST request passes correctly.
        '''

        # Make a POST request to trigger the view
        response = self.client.post(reverse('home'), {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        })

        # Check that the response is a redirect (status code 302)
        self.assertTrue(200 <= response.status_code < 400)

    # def test_index_view_POST_email_bot(self):
    #     '''
    #     Testing to see if a POST request fails when a bot enters information.
    #     '''

    #     # Make a POST request to trigger the view
    #     response = self.client.post(reverse('home'), {
    #         'name': 'John Doe',
    #         'email': 'johndoe@example.com',
    #         'subject': 'Test Subject',
    #         'message': 'Test message content',
    #         'honeypot':'Filling this to simulate a bot'
    #     })

    #     # Check that the response is a redirect (status code 400)
    #     self.assertTrue(response.status_code == 400)

    @patch('RRRApp.views.emailMessage') # Mock the emailMessage function in RRRApp.views for testing
    def test_email_sending(self, mock_email_message):
        '''
        Testing to see if the email is sent correctly. 
        Note, it does actually send the email it just tests if the function would run.
        If the email sending were to fail, it would be on our SMTP server's end and there is nothing we can do about it.
        '''

        response = self.client.post(reverse('home'), {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        })

        self.assertTrue(200 <= response.status_code < 400)

    @patch('RRRApp.views.emailMessage')
    def test_backend_processing_error(self, mock_email_message):
        '''
        Simulating the email failing to send but make sure nothing breaks.
        '''

        # Set up the mock to raise an exception when called
        mock_email_message.side_effect = ValidationError('Email sending failed')

        response = self.client.post(reverse('home'), {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        })

        # Check that the response is a redirect (status code 302)
        self.assertTrue(200 <= response.status_code < 400)

class MerchTestCase(TestCase):
    '''
    All tests associated with merch.py
    '''

    def test_merchMessageFormat_noSize(self):
        '''
        Tests merch with no size.
        '''

        name = "John Doe"
        email = "john.doe@example.com"
        size = None
        item = '2023-24 RRR Sticker'

        # Call the function with the test input
        formatted_message = merchMessageFormat(name, item, size)

        # Check the expected output
        expected_message = f'John Doe is wondering if we have a 2023-24 RRR Sticker available for purchase.'
        self.assertEqual(formatted_message, expected_message)

    def test_merchMessageFormat_size(self):
        '''
        Tests merch with a size attached.
        '''

        name = "John Doe"
        size = 'xl'
        item = '2023-24 Team T-shirt'

        # Call the function with the test input
        formatted_message = merchMessageFormat(name, item, size)

        # Check the expected output
        expected_message = f'John Doe is wondering if we have a 2023-24 Team T-shirt in a size XL available for purchase.'
        self.assertEqual(formatted_message, expected_message)


class YourViewsTests(TestCase):
    '''
    Test cases for views.py.
    '''

    def setUp(self):
        '''
        Set up the testing environment, including creating a client for making requests.
        '''
        self.client = Client()
        # Other setup code as needed

    def test_index_view(self):
        '''
        Test the index view to ensure a successful response (status code between 200 and 400).
        '''
        response = self.client.get(reverse('home'))
        self.assertTrue(200 <= response.status_code < 400)

    def test_team_view(self):
        '''
        Test the team view to ensure a successful response (status code between 200 and 400).
        '''
        response = self.client.get(reverse('team'))
        self.assertTrue(200 <= response.status_code < 400)

    def test_cars_view(self):
        '''
        Test the cars view to ensure a successful response (status code between 200 and 400).
        '''
        response = self.client.get(reverse('cars'))
        self.assertTrue(200 <= response.status_code < 400)

    def test_sponsor_view(self):
        '''
        Test the sponsor view to ensure a successful response (status code between 200 and 400).
        '''
        response = self.client.get(reverse('sponsor'))
        self.assertTrue(200 <= response.status_code < 400)

    def test_carshow_view_GET(self):
        '''
        Test the carshow view for a GET request to ensure a successful response (status code between 200 and 400).
        '''
        response = self.client.get(reverse('carshow'))
        self.assertTrue(200 <= response.status_code < 400)

    def test_faq_view(self):
        '''
        Test the FAQ view to ensure a successful response (status code between 200 and 400).
        '''
        response = self.client.get(reverse('faq'))
        self.assertTrue(200 <= response.status_code < 400)

    def test_privacy_view(self):
        '''
        Test the privacy view to ensure a successful response (status code between 200 and 400).
        '''
        response = self.client.get(reverse('privacy'))
        self.assertTrue(200 <= response.status_code < 400)

    def test_terms_view(self):
        '''
        Test the terms view to ensure a successful response (status code between 200 and 400).
        '''
        response = self.client.get(reverse('terms'))
        self.assertTrue(200 <= response.status_code < 400)

    def test_robots_view(self):
        '''
        Test the robots view to ensure a successful response (status code between 200 and 400).
        '''
        response = self.client.get(reverse('robots'))
        self.assertTrue(200 <= response.status_code < 400)