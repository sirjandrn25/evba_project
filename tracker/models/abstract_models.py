from django.db import models
from django.db.models.enums import Choices
from django.contrib.auth.hashers import make_password


class TimeDateTracker(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    


class Person(TimeDateTracker):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150,unique=True,blank=False)
    password = models.CharField(max_length=150)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.full_name
    
    def save(self,*args,**kwargs):
        if self.id is None:
            self.password = make_password(self.password)
        return super(Person,self).save(*args,**kwargs)


class Location(models.Model):
    address_name = models.CharField(max_length=150,blank=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    class Meta:
        abstract = True

class AbstractProfile(models.Model):
    gender_choices = (
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
    )
    gender = models.CharField(max_length=10,choices=gender_choices,default="male")
    birth_date = models.DateField(blank=True,null=True)
    avatar = models.ImageField(upload_to="profile/",blank=True,null=True)
    is_approve = models.BooleanField(default=False)
    # is_verify = models.BooleanField(default=False)
    # verify_token = models.CharField(max_length=200)
    contact_no = models.CharField(max_length=20,blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract=True
    



    

