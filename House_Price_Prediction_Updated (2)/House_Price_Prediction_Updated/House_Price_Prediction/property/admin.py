from django.contrib import admin

# Register your models here.
from .models import Property
admin.site.register(Property)

admin.site.site_header = "House Price Prediction Admin"
admin.site.site_title = "House Price Prediction Admin Portal"
admin.site.index_title = "House Price Prediction Management"
