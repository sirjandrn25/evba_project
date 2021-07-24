from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from tracker.forms import *
from django.contrib import messages
from django.utils.decorators import method_decorator
from tracker.decorators import *
from tracker.forms import *
from tracker.utils import *

class DriverIndexView(View):
    @method_decorator(IsDriverLogged)
    def get(self,request):
        request.session['running_mechanic_list'] = []
        request.session['mechanic_list'] = {
            'data':[],
            'index':0
        }
        form = HelpForm(data=request.GET)
        if form.is_valid():
            print("valid")
        else:
            
            context = {
                'form':form
            }
            return render(request,"driver/index.html",context)


class DriverAccountView(View):
    def get(self,request):
        driver = get_object_or_404(Driver.objects.all(),pk=request.session['driver_id'])
        driver_form = DriverForm(instance=driver)
        driver_profile_form = DriverProfileForm(instance=driver.driver_profile)
        

        context = {
            'driver_form':driver_form,
            'driver_profile_form':driver_profile_form,
            'driver':driver

        }


        return render(request,"driver/account.html",context)
    def post(self,request):
        driver = get_object_or_404(Driver.objects.all(),pk=request.session['driver_id'])
        driver_form = DriverForm(instance=driver,data=request.POST)
        driver_profile_form = DriverProfileForm(instance=driver.driver_profile,data=request.POST,files=request.FILES)
        if driver_form.is_valid():
            driver_form.save()
        else:
            print(driver_form.errors)

        if driver_profile_form.is_valid():
            driver_profile_form.save()
        else:
            messages.info(request,"successfully update the new message")
            return redirect('driver_account')

        context = {
            'driver_form':driver_form,
            'driver_profile_form':driver_profile_form,
            'driver':driver

        }
        return render(request,"driver/account.html",context)


class DriverSignUpView(View):

    def get(self,request):
        form = DriverSignUpForm()
        context = {
            'form':form
        }
        return render(request,"driver/signup.html",context)
    
    def post(self,request):
        form = DriverSignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,"Successfully create driver account")
            return redirect("driver_signup")
            

        else:
            context = {
                'form':form
            }
            return render(request,"driver/signup.html",context)


class DriverLoginView(View):
    def get(self,request):
        try:
            request.session['driver_id']
            return redirect("driver_index")
        except:
            form = DriverLoginForm()
            
            context = {
                'form':form
            }
            return render(request,"driver/login.html",context)
    
    def post(self,request):
        form = DriverLoginForm(data=request.POST)
        if form.is_valid():
            driver = form.cleaned_data.get('driver')
            request.session["driver_id"] = driver.id
            return redirect("driver_index")
        else:
            print(form.errors)
            context = {
                'form':form
            }
            return render(request,"driver/login.html",context)
        
        return redirect("driver_login")

class DriverLogoutView(View):
    @method_decorator(IsDriverLogged)
    def get(self,request):
        del request.session['driver_id']
        messages.info(request,"Driver Successfully logout")
        return redirect("driver_login")







from tracker.serializers import *
def available_mechanics(request):
    serializer = MechanicSerializer(Mechanic.objects.all(),many=True)


    return render(request,"driver/search_mechanics.html")

from rest_framework.views import APIView
from rest_framework.response import Response

class FetchMechanicData(APIView):
    def get(self,request):
    
        serializer = MechanicSerializer(Mechanic.objects.all(),many=True)
        
        return Response(serializer.data,status=200)
    def post(self,request):
        search_range = request.data['search_range']
        curr_location = request.data['curr_location']
        available_mechanic_list = []
        
        for m_p in MechanicProfile.objects.filter(is_approve=True):
            dest_location  = {
                'lat':m_p.latitude,
                'lon':m_p.longitude
            }
            d = distance(curr_location,dest_location)
            if d<=int(search_range):
                serializer = MechanicSerializer(m_p.mechanic)
                available_mechanic_list.append(serializer.data)
        return Response(available_mechanic_list,status=200)

            



    

class FeedbackView(APIView):

    def get(self,request):
        mechanic = request.GET.get('mechanic')
        if mechanic:
            mechanic_obj = Mechanic.objects.get(id=mechanic)
        
            feedbacks = Feedback.objects.filter(mechanic=mechanic_obj)
        else:
            feedbacks = Feedback.objects.all()

        serializer = FeedbackSerializer(feedbacks,many=True)


        return Response(serializer.data,status=200)
    
    def post(self,request):
        mechanic= request.data['mechanic']
        driver = request.session['driver_id']
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            feedback_obj = serializer.save(driver=driver,mechanic=mechanic)
            serializer = FeedbackSerializer(feedback_obj,many=False)
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=404)
        