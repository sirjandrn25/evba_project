from tracker.models import *
from tracker.serializers import *


for m_profile in MechanicProfile.objects.all():
    print(m_profile)