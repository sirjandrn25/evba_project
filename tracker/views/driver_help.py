
from django.core.checks import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from tracker.decorators import IsDriverLogged
from rest_framework.views import APIView
from rest_framework.response import Response
from tracker.serializers import *
from tracker.utils import *
from tracker.utils import *
from tracker.models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_notification(msg,room_name):
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(room_name,
        {
            'type':'fetch_help',
            'text':msg
        }
    )


class SendHelpView(APIView):

    def post(self,request):
        data = request.data
        search_range = request.data.get('range')

        curr_loc ={
            'lat':data.get('curr_driver_lat'),
            'lon':data.get('curr_driver_long')
        }
        curr_mechanic_list = get_mechanic_list(curr_loc,search_range)
        prev_mechanic_list = request.session['mechanic_list']['data']
        
        index = request.session['mechanic_list']['index']
        if prev_mechanic_list:
            mechanic_list = [mechanic for mechanic in curr_mechanic_list if mechanic not in prev_mechanic_list]
            curr_mechanic_list = prev_mechanic_list.extend(mechanic_list)
        new_info = {
            'data':curr_mechanic_list,
            'index':index
        }
      
        request.session['mechanic_list'] = new_info
        running_mechanic_list = request.session['running_mechanic_list']
        if running_mechanic_list:
            available_mechanic = available_running_mechanic(request)
            
        else:
            available_mechanic = return_not_running_mechanic(request)
        print(available_mechanic)
        if available_mechanic:
            mechanic = available_mechanic['mechanic']
            distance = available_mechanic['distance']
            service = request.data['service']
            serializer = HelpSerializer(data=request.data)
            if serializer.is_valid():
                help_obj = serializer.save(driver=request.session['driver_id'],mechanic=mechanic,service=service)
                help_obj.mechanic.mechanic_profile.is_busy=True
                help_obj.mechanic.mechanic_profile.save()
                serializer = HelpSerializer(help_obj)
                data = serializer.data
                data['distance'] = distance
                room_name=f"mechanic_{mechanic}"
                request.session['prev_help_info'] =data
                send_notification(room_name=room_name,msg=data)
                return Response(data,status=200)
            
            return Response(serializer.errors,status=404)
        
        resp = {
            'detail':"not mechanic available"
        }
        return Response(resp,status=404)








class SendHelpRequestAgain(APIView):
    def get(self,request):

        prev_help_info = request.session['prev_help_info']
        prev_mechanic_id = prev_help_info['mechanic']['id']
        prev_mechanic = Mechanic.objects.get(id=prev_mechanic_id)
        available_mechanic = available_running_mechanic(request)
        prev_mechanic.mechanic_profile.is_busy=False
        prev_mechanic.mechanic_profile.save()
        
        if len(list(available_mechanic.keys())) == 0:
            
            available_mechanic = return_not_running_mechanic(request)
            if len(list(available_mechanic.keys())) == 0:
                resp = {
                    'detail':"mechanic is not available",
                    'status':404
                }

                return Response(resp,status=404)
        
        # print(available_mechanic)
        serializer = HelpSerializer(data=prev_help_info)
        if serializer.is_valid():
            distance = available_mechanic['distance']
            mechanic = available_mechanic['mechanic']
            service = prev_help_info['service']['id']
            help_obj = serializer.save(driver=request.session['driver_id'],mechanic=mechanic,service=service)
            help_obj.mechanic.mechanic_profile.is_busy=True
            help_obj.mechanic.mechanic_profile.save()
            serializer = HelpSerializer(help_obj)
            data = serializer.data
            data['distance'] = distance
            room_name=f"mechanic_{mechanic}"
            request.session['prev_help_info'] =data
            send_notification(room_name=room_name,msg=data)
            return Response(data,status=200)



def return_not_running_mechanic(request):
    index = request.session['mechanic_list']['index']
    remaining_mechanic_list = request.session['mechanic_list']['data'][index:]
    running_mechanic_list = request.session['running_mechanic_list']
    available_mechanic = {}
   
    for i in range(len(remaining_mechanic_list)):
        mechanic = Mechanic.objects.filter(id=remaining_mechanic_list[i]['mechanic']).first()
        available_mechanic = remaining_mechanic_list[i]
       
        if mechanic.mechanic_profile.is_busy:
            index +=1
            try:
                running_mechanic_list.index(remaining_mechanic_list[i])
            except :
                running_mechanic_list.append(remaining_mechanic_list[i])
        else:
            break

    request.session['running_mechanic_list'] = running_mechanic_list
    mechanic_list = request.session['mechanic_list']['data']
    if len(mechanic_list)>index:
        request.session['mechanic_list'] = {
            'data':mechanic_list,
            'index':index+1
            }

        return available_mechanic
    else:
        request.session['mechanic_list'] = {
        'data':mechanic_list,
        'index':index
        }

        return {}

def available_running_mechanic(request):
   
    data = request.session['running_mechanic_list']
    mechanic_info = {}

    
    for d in data:
        mechanic = Mechanic.objects.filter(id=d['mechanic']).first()
        if mechanic.mechanic_profile.is_busy == False:
            
            mechanic_info = d
            break
    
    if mechanic_info:
        data.remove(mechanic_info)
    request.session['running_mechanic_list'] = data
    return mechanic_info



def get_mechanic_list(curr_location,search_range):
    
    available_mechanic_list = []
    for m_p in MechanicProfile.objects.filter(is_approve=True):
        dest_location  = {
            'lat':m_p.latitude,
            'lon':m_p.longitude
        }
        d = distance(curr_location,dest_location)
        print(dest_location)
        if d<=search_range:
            available_mechanic_list.append({
                'mechanic':m_p.mechanic.id,
                'distance':d
            })
    sort_data = bubble_sort(available_mechanic_list)
    return sort_data





        
                


    
    
