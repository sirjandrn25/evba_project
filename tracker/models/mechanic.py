from django.db.models.base import Model
from .abstract_models import *
from django.db import models
from .service import *



class Mechanic(Person):
    pan_no = models.CharField(max_length=150,blank=False,unique=True)

class MechanicProfile(AbstractProfile,Location):
    services = models.ManyToManyField(Service)
    is_busy = models.BooleanField(default=False)
    mechanic = models.OneToOneField(Mechanic,on_delete=models.CASCADE,related_name="mechanic_profile")
    
    def __str__(self):
        return self.mechanic.full_name



    
