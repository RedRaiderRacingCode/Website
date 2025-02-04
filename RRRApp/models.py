from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class MerchItem(models.Model):
    image = models.ImageField(upload_to='merchItems/', help_text="Upload the image of the merch item. Preferably a .png file with no background.")
    secondary_image = models.ImageField(upload_to='merchItems/', help_text="Upload the secondary image of the merch item. This could be the back of the shirt. Preferably a .png file with no background. (Optional)", blank=True, null=True)
    item_name = models.CharField(max_length=200, help_text="Enter the item's name. Do not include an underscore ('_') in the name.")
    price = models.DecimalField(
            max_digits=6, decimal_places=2,
            validators=[MinValueValidator(0.00), MaxValueValidator(9999.99)],
            help_text="Enter the item's price."
        )  # Maximum cost set to 9999 with 2 decimal places
    size = models.BooleanField(help_text="Toggle on if a size section should be included. Ex: Shirts.")

    def __str__(self) -> str:
        return self.item_name

class AdminTeamMember(models.Model):
    headshot = models.ImageField(upload_to='adminMembers/', help_text="Upload a headshot image of the member in a 1x1 format.")
    member_name = models.CharField(max_length=200, help_text="Enter the member's name.")
    title = models.CharField(max_length=200, help_text="Enter the member's title.")
    sub_section = models.CharField(max_length=200, help_text="Enter the member's sub_section. Ex. Aero, Powertrain, Electrical, etc. This is used for ordering the team page.", default=None)
    first = models.BooleanField(help_text="Toggle on if the member should be first. Ex: President. This is used for ordering the team page.", default=False)
    school_email = models.EmailField(max_length=200, help_text="Enter the member's school email address. Ex: raiderred@ttu.edu.")
    linkedIn = models.URLField(max_length=500, help_text="Enter the member's LinkedIn profile URL. (Optional)", blank=True, null=True)

    def __str__(self) -> str:
        return self.member_name
    
class TechincalTeamMember(models.Model):
    headshot = models.ImageField(upload_to='technicalMembers/', help_text="Upload a headshot image of the member in a 1x1 format." )
    member_name = models.CharField(max_length=200, help_text="Enter the member's name.")
    title = models.CharField(max_length=200, help_text="Enter the member's title.")
    sub_section = models.CharField(max_length=200, help_text="Enter the member's sub_section. Ex. Aero, Powertrain, Electrical, etc. This is used for ordering the team page.", default=None)
    first = models.BooleanField(help_text="Toggle on if the member should be first. Ex: President. This is used for ordering the team page.", default=False)
    school_email = models.EmailField(max_length=200, help_text="Enter the member's school email address. Ex: raiderred@ttu.edu.")
    linkedIn = models.URLField(max_length=500, help_text="Enter the member's LinkedIn profile URL. (Optional)", blank=True, null=True)

    def __str__(self) -> str:
        return self.member_name

class Car(models.Model):
    car_name = models.CharField(max_length=50, help_text="Enter the name of the car in the format: RRR-YYYY. Ex: RRR-2023.")
    image = models.ImageField(upload_to='cars/', help_text="Upload an image of the car.")
    chassis = models.CharField(max_length=200, help_text="Enter the chassis details of the car. (Optional)", blank=True, null=True)
    power_unit = models.CharField(max_length=200, help_text="Enter the power unit details of the car. (Optional)", blank=True, null=True)
    weight = models.IntegerField(help_text="Enter the weight of the car. (Optional)",blank=True,null=True)
    main_achievement = models.TextField(max_length=200, help_text="Enter the car's main achievement. (Optional)", blank=True)
    competition_placement = models.CharField(max_length=200, help_text="Enter the car's competition placement. Format: placement/# of teams. Ex: 50/120. (Optional)", blank=True)

    def __str__(self) -> str:
        return self.car_name
    
class CarShow(models.Model):
    year = models.IntegerField(help_text="Enter the year of the car show in the format YYYY. Ex: 2023.")
    date = models.DateField(help_text="Enter the date the car show will take place.", default=None)
    start_time = models.CharField(max_length=8,help_text="Enter the time the car show will start. Format: TT:TT AM. Ex: 9:00 AM. (Optional)", default=None, null=True, blank=True)
    end_time = models.CharField(max_length=8,help_text="Enter the time the car show will end. Format: TT:TT PM. Ex: 9:00 PM. (Optional)", default=None, null=True, blank=True)
    location_name = models.CharField(max_length=200, help_text='Enter the name of the location. This will be used when sending emails to people who register. Ex: Commuter North Parking Lot.', default='Unknown')
    location_HTML = models.TextField(max_length=2000, help_text='Enter the location of the car show in the format of an embedded HTML Google Map location. Tutorial on how to do this: <a href="https://support.google.com/maps/answer/144361?hl=en&co=GENIE.Platform%3DDesktop" target="_blank">Google Map</a>.')
    email_preregister_payment_link = models.URLField(max_length=500, help_text='Enter the url to that will direct the user to the preregister payment.', default=None)
    preregister_cost = models.DecimalField(
            max_digits=5, decimal_places=2,
            validators=[MinValueValidator(0.00), MaxValueValidator(999.99)],
            help_text="Enter the cost of registering a car early.", default=None
        )  # Maximum cost set to 999 with 2 decimal places
    register_cost = models.DecimalField(
            max_digits=5, decimal_places=2,
            validators=[MinValueValidator(0.00), MaxValueValidator(999.99)],
            help_text="Enter the cost of registering a car at the entrance.", default=None
        )  # Maximum cost set to 999 with 2 decimal places
    show_registration = models.BooleanField(help_text="Toggle off if you want to hide the registration. Ex: After the car show you won't want people still registering.", default=True, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.year)
    
class FAQQuestion(models.Model):
    question = models.CharField(max_length=200,help_text="Enter the frequently asked question.")
    answer = models.TextField(max_length=2000, help_text='Enter the answer to the FAQ.')
    first = models.BooleanField(help_text="Toggle on if the question should be first after how to join. Ex: General body meetings. This is used for ordering the FAQ page.", default=False)

    def __str__(self) -> str:
        return self.question
    
class CarShowAttendee(models.Model):
    first_name = models.CharField(max_length=200,help_text="Enter the attendee's first name.")
    last_name = models.CharField(max_length=200,help_text="Enter the attendee's last name.")
    email = models.CharField(max_length=200,help_text="Enter the attendee's email.")
    section = models.CharField(max_length=200,help_text="Enter the attendee's section.")
    paid = models.BooleanField(help_text='Check if the attendee has paid.',default=False)

    def __str__(self) -> str:
        return self.first_name +' '+ self.last_name

class Sponsor(models.Model):
    sponsor_name = models.CharField(max_length=200,help_text="Enter the sponsor's name.")
    sponsor_logo = models.ImageField(upload_to='sponsors/', help_text="Upload an image of the sponsors logo. Make sure the background is either transparent or white. ")
    sponsor_link = models.URLField(max_length=500, help_text="Enter the URL to the sponsor's website. This is so that people can easily click on the image and go straight to the sponsor's page. (Optional only if they do not have one)", blank=True, null=True)

    def __str__(self) -> str:
        return self.sponsor_name
