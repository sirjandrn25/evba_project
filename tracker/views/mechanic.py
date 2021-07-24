from django.views import View
from django.shortcuts import get_object_or_404, redirect,render
from tracker.forms import *
from django.contrib import messages
from tracker.decorators import *
from django.utils.decorators import method_decorator



class MechanicIndexView(View):
    @method_decorator([IsMechanicLogged,IsMechanicInitialUpdate])
    def get(self,request):
        # del request.session['mechanic_id']
        mechanic_id= request.session['mechanic_id']
        try:
            mechanic = Mechanic.objects.get(id=mechanic_id)
        except:
            print("error")
        context = {
            "mechanic_name":mechanic.full_name
        }
        return render(request,"mechanic/index.html",context)

class MechanicAccountView(View):
    def get(self,request):
        mechanic = get_object_or_404(Mechanic.objects.all(),pk=request.session['mechanic_id'])
        mechanic_form = MechanicForm(instance=mechanic)
        mechanic_profile_form = MechanicProfileForm(instance=mechanic.mechanic_profile)

        context = {
            'mechanic':mechanic,
            'mechanic_form':mechanic_form,
            'mechanic_profile_form':mechanic_profile_form
        }
        return render(request,"mechanic/account.html",context)
    
    def post(self,request):
        mechanic = get_object_or_404(Mechanic.objects.all(),pk=request.session['mechanic_id'])
        mechanic_form = MechanicForm(instance=mechanic,data=request.POST)
        mechanic_profile_form = MechanicProfileForm(instance=mechanic.mechanic_profile,data=request.POST,files=request.FILES)

        if mechanic_form.is_valid():
            mechanic_form.save()
        
        if mechanic_profile_form.is_valid():
            mechanic_profile_form.save()
        context = {
            'mechanic':mechanic,
            'mechanic_form':mechanic_form,
            'mechanic_profile_form':mechanic_profile_form
        }
        return render(request,"mechanic/account.html",context)
        

class MechanicLoginView(View):
    def get(self,request):
        try:
            request.session['mechanic_id']
            return redirect("mechanic_index")
        except:
            form = MechanicLoginForm()
            context = {
                'form':form
            }
            return render(request,"mechanic/login.html",context)
    def post(self,request):
        form = MechanicLoginForm(data=request.POST)
        if form.is_valid():
            mechanic = form.cleaned_data['mechanic']
            request.session['mechanic_id'] = mechanic.id
            return redirect("mechanic_index")
        else:
            context = {
                'form':form
            }
            return render(request,"mechanic/login.html",context)

class MechanicSignUpView(View):

    def get(self,request):
        form = MechanicSignUpForm()
        context = {
            'form':form
        }
        return render(request,"mechanic/signup.html",context)
    
    def post(self,request):
        form = MechanicSignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,"Successfully create mechanic account")
            return redirect("mechanic_signup")

        else:
            context = {
                'form':form
            }
            return render(request,"mechanic/signup.html",context)
    

class MechanicLogoutView(View):
    @method_decorator(IsMechanicLogged)
    def get(self,request):
        del request.session['mechanic_id']
        messages.info(request,"Mechanic Successfully logout")
        return redirect("mechanic_login")


class MechanicInitialUpdate(View):
    @method_decorator(IsMechanicLogged)
    def get(self,request):
        
        return render(request,"mechanic/initialUpdate.html")

    def post(self,request):
        address = request.POST.get('address')
        try:
            latitude = float(request.POST.get('latitude'))
            longitude = float(request.POST.get('longitude'))
        except:
            print("error")
        if address and latitude and longitude:
            mechanic_id= request.session['mechanic_id']
            try:
                mechanic = Mechanic.objects.get(id=mechanic_id)
                profile = MechanicProfile.objects.get(mechanic=mechanic)
            except:
                print("error")
            profile.address_name = address
            profile.latitude = latitude
            profile.longitude = longitude
            profile.is_active = True
            profile.save()
            return redirect("mechanic_index")
        else:
            messages.error(request,"Address of mechanic is must required")
            return redirect("mechanic_initial_update")
        


from rest_framework.views import APIView
from rest_framework.response import Response

class SendResponseView(APIView):
    def post(self,request):
        data = request.data
       
        
        send_driver_notification(data)
        
        mechanic = Mechanic.objects.get(id=data['mechanic']['id'])
        mechanic.mechanic_profile.is_busy=False
        mechanic.mechanic_profile.save()
        try:
            help = Help.objects.get(id=data['id'])
            help.is_accept=True
            help.save()
        except Exception as e:
            print(e)
            
        resp = {
            'status':200
        }
        return Response(resp)


def send_driver_notification(data):
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    channel_layer = get_channel_layer()
    room_name = f"driver_{data['driver']['id']}"
    async_to_sync(channel_layer.group_send)(room_name,
        {
            'type':'fetch_response',
            'text':data
        }
    )
