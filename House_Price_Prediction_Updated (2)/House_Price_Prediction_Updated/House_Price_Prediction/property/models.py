from django.db import models

# Create your models here.
class Property(models.Model):
    area = models.FloatField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    stories = models.IntegerField()
    mainroad = models.BooleanField()
    guestroom = models.BooleanField()
    basement = models.BooleanField()
    hotwaterheating = models.BooleanField()
    airconditioning = models.BooleanField()
    parking = models.IntegerField()
    prefarea = models.BooleanField()
    furnishingstatus = models.CharField(max_length=255)
    predictedprice = models.IntegerField()

    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    area_unit = models.CharField(max_length=10, null=True, blank=True)
    costpersqunit = models.DecimalField(max_digits=10, decimal_places=2)
    final_estimation = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"Property in {self.city}, {self.state} - {self.predictedprice}"

    