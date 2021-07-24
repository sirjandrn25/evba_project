from django.db import models
from .abstract_models import TimeDateTracker
from tracker.models import *


class Help(TimeDateTracker):
    vehicle_choices = (
        ('two_wheeler','Two wheeler'),
        ('four_wheeler','Four Wheeler')
    )
    driver = models.ForeignKey(Driver,on_delete=models.CASCADE,related_name="help")
    mechanic = models.ForeignKey(Mechanic,on_delete=models.CASCADE,related_name="help")
    is_accept = models.BooleanField(default=False)
    vehicle_type = models.CharField(max_length=20,choices=vehicle_choices,default="two_wheeler")
    problem_desc = models.TextField(blank=True)
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    curr_driver_lat = models.FloatField()
    curr_driver_long = models.FloatField()


    
    def __str__(self):
        return f"driver: {self.driver} mechanic: {self.mechanic} "


class Feedback(TimeDateTracker):
    driver = models.ForeignKey(Driver,on_delete=models.CASCADE,related_name="feedback")
    mechanic = models.ForeignKey(Mechanic,on_delete=models.CASCADE,related_name="feedback")
    message = models.TextField()

    


    