from .abstract_models import *
from django.db import models


class Driver(Person):
    license_no = models.CharField(max_length=100)


class DriverProfile(AbstractProfile):
    address = models.CharField(max_length=150,blank=True)
    driver = models.OneToOneField(Driver,on_delete=models.CASCADE,related_name="driver_profile")
    is_busy=models.BooleanField(default=False)

    def __str__(self):
        return self.driver
    

