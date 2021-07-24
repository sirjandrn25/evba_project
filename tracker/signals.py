from django.db.models.signals import post_save
from django.dispatch import receiver
from tracker.models import *
# from tracker.utils import get_current_location


@receiver(post_save, sender=Mechanic)
def mechanic_profile_creation(sender, **kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        # location = get_current_location()
        # address = location.get('address')
        # lat = location.get('lat')
        # lon = location.get('lon')
        profile = MechanicProfile(mechanic=instance)
        profile.save()

@receiver(post_save,sender=Driver)
def driver_profile_creation(sender,**kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        profile = DriverProfile(driver=instance)
        profile.save()



