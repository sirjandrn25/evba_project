from django.contrib import messages
from django.shortcuts import redirect,render
from tracker.models import *


def IsDriverLogged(view):
    def wrapper(request,*args,**kwargs):
        try:
            request.session['driver_id']
        except Exception as e:
            messages.error(request,"First driver Login is required !!!")
            return redirect("driver_login")
        return view(request,*args,**kwargs)

    return wrapper

def IsMechanicLogged(view):
    def wrapper(request,*args,**kwargs):
        
        try:
            request.session['mechanic_id']
        except Exception as e:
            print("mechanic logged")
            messages.error(request,"First mechanic Login is required !!!")
            return redirect("mechanic_login")
        return view(request,*args,**kwargs)

    return wrapper

def IsMechanicInitialUpdate(view):
   
    def wrapper(request,*args,**kwargs):
        try:
            mechanic_id = request.session['mechanic_id']
            mechanic = Mechanic.objects.get(id=mechanic_id)
            profile = MechanicProfile.objects.get(mechanic=mechanic)
        except Exception as e:
            print(e)
        
        if profile.latitude and profile.longitude:
            return view(request,*args,**kwargs)
        else:
            return redirect("mechanic_initial_update")
    return wrapper


