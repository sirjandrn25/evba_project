import re
from tracker.models.help import Help
from rest_framework import serializers
from tracker.models import *


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id','service_name','image']
        read_only_fields = ['id']


class MechanicProfileSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(read_only=True,many=True)
    class Meta:
        model = MechanicProfile
        fields = ('address_name','latitude','longitude','contact_no','services')

class MechanicSerializer(serializers.ModelSerializer):
    mechanic_profile = MechanicProfileSerializer()
    class Meta:
        model = Mechanic
        fields = ('id','full_name','mechanic_profile')
        read_only_fields = ['id']




class DriverProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DriverProfile
        fields = ('contact_no',)
        


class DriverSerializer(serializers.ModelSerializer):
    driver_profile = DriverProfileSerializer(read_only=True,many=False)
    class Meta:
        model = Driver
        fields= ('id','full_name','driver_profile')
        read_only_fields = ['id']




class HelpSerializer(serializers.ModelSerializer):
    mechanic = MechanicSerializer(read_only=True,many=False)
  
    driver = DriverSerializer(read_only=True,many=False)
    service = ServiceSerializer(read_only=True,many=False)
    

  
    
    
    
    class Meta:
        model = Help
        fields = ["id","vehicle_type","service","problem_desc","mechanic","driver",'curr_driver_lat','curr_driver_long']
        read_only_fields = ['id']
    
    def save(self,driver,mechanic,service):
        validated_data = self.validated_data
        mechanic = Mechanic.objects.filter(id=mechanic).first()
        driver = Driver.objects.filter(id=driver).first()
        service = Service.objects.get(id=service)
        validated_data['mechanic'] = mechanic
        validated_data['driver'] = driver
        validated_data['service'] =service
        return Help.objects.create(**validated_data)




class FeedbackSerializer(serializers.ModelSerializer):
    mechanic = MechanicSerializer(read_only=True,many=False)
    driver = DriverSerializer(read_only=True,many=False)
    class Meta:
        model = Feedback
        fields = "__all__"
    
    def save(self,driver,mechanic):
        validated_data = self.validated_data
        mechanic = Mechanic.objects.filter(id=mechanic).first()
        driver = Driver.objects.filter(id=driver).first()
        validated_data['mechanic']=mechanic
        validated_data['driver']=driver
        return Feedback.objects.create(**validated_data)
        





# >>> from tracker.models import *
# >>> from tracker.serializers import *
# >>> data={}
# >>> data['service']=1
# >>> data['vehicle_type'] = 'two_wheeler'
# >>> data['curr_driver_lat']=25.45
# >>> data['curr_driver_long']=25.45
# >>> serializer = HelpSerializer(data=data)