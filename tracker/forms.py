from django import forms
from django.forms import widgets
from tracker.models import *
from django.contrib.auth.hashers import check_password
# from django.forms import Form


class DriverLoginForm(forms.Form):
    email = forms.CharField(max_length=150,widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email address'}))
    password = forms.CharField(max_length=150,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password'}))

    def clean(self):
        validated_data = super().clean()
        email = validated_data.get('email','')
        password = validated_data.get('password','')
        if email and password:
            try:
                driver = Driver.objects.get(email=email)
            except:
                raise forms.ValidationError("This email id doesn't exists !!")
            if check_password(password,driver.password):
                validated_data['driver'] = driver
                return validated_data
            else:
                raise forms.ValidationError("Password is not matched !!")
        else:
            raise forms.ValidationError("Both Field are must required !!")

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"
        exclude = ("password",)
        widgets = {
            'full_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Full Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email address','readonly':True}),
            'license_no':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Liscence number'})
        }

class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = "__all__"
        exclude = ('driver',"is_approve","is_busy","is_active")
        widgets = {
            'gender':forms.Select(attrs={'class':'form-select'}),
            'birth_date':forms.DateInput(attrs={'class':'form-control','placeholder':'YYYY-MM-DD'}),
            'contact_no':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Contact number'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Address'}),
            'avatar':forms.FileInput(attrs={'class':'form-control'})
        }
        

class DriverSignUpForm(forms.ModelForm):
    password = forms.CharField(max_length=150,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password'}))
    re_password = forms.CharField(max_length=150,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter confirm password'}))
    class Meta:
        model = Driver
        fields = ('full_name','email','license_no','password','re_password')
        widgets = {
            'full_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Full Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email address'}),
            'license_no':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Liscence number'})
        }
    
    def clean(self):
        validated_data = super().clean()
        password = validated_data.get('password','')
        re_password = validated_data.get('re_password','')
        if password and re_password:
            if password !=re_password:
                error = "Both password is not matched !!!"
            elif len(password)<7:
                error = "At least 7 charectors are required is password"
            elif password.isdigit():
                error = "only numeric values are not allowed"
            else:
                return validated_data
        raise forms.ValidationError(error)
    
    def save(self,*args,**kwargs):
        cleaned_data = self.cleaned_data
        full_name=cleaned_data.get('full_name')
        email=cleaned_data.get('email')
        password=cleaned_data.get('password')
        license_no=cleaned_data.get('license_no')

        driver = Driver(full_name=full_name,email=email,password=password,license_no=license_no)
        driver.save()



class MechanicSignUpForm(forms.ModelForm):
    password = forms.CharField(max_length=150,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password'}))
    re_password = forms.CharField(max_length=150,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter confirm password'}))
    class Meta:
        model = Mechanic
        fields = ('full_name','email','pan_no','password','re_password')
        widgets = {
            'full_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Full Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email address'}),
            'pan_no':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter pan number'})
        }
    
    def clean(self):
        validated_data = super().clean()
        password = validated_data.get('password','')
        re_password = validated_data.get('re_password','')
        if password and re_password:
            if password !=re_password:
                error = "Both password is not matched !!!"
            elif len(password)<7:
                error = "At least 7 charectors are required is password"
            elif password.isdigit():
                error = "only numeric values are not allowed"
            else:
                return validated_data
        raise forms.ValidationError(error)
    
    def save(self,*args,**kwargs):
        cleaned_data = self.cleaned_data
        full_name=cleaned_data.get('full_name')
        email=cleaned_data.get('email')
        password=cleaned_data.get('password')
        pan_no=cleaned_data.get('pan_no')

        mechanic = Mechanic(full_name=full_name,email=email,password=password,pan_no=pan_no)
        mechanic.save()

class MechanicLoginForm(forms.Form):
    email = forms.CharField(max_length=150,widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email address'}))
    password = forms.CharField(max_length=150,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password'}))

    def clean(self):
        validated_data = super().clean()
        email = validated_data.get('email','')
        password = validated_data.get('password','')
        if email and password:
            try:
                mechanic = Mechanic.objects.get(email=email)
            except:
                raise forms.ValidationError("This email id doesn't exists !!")
            if check_password(password,mechanic.password):
                validated_data['mechanic'] = mechanic
                return validated_data
            else:
                raise forms.ValidationError("Password is not matched !!")
        else:
            raise forms.ValidationError("Both Field are must required !!")


class MechanicForm(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = "__all__"
        widgets = {
            'full_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Full Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email address','readonly':True}),
            'pan_no':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter pan number'})
        }
        exclude = ("password",)

class MechanicProfileForm(forms.ModelForm):
    class Meta:
        model = MechanicProfile
        fields = "__all__"

        widgets = {
            'gender':forms.Select(attrs={'class':'form-select'}),
            'birth_date':forms.DateInput(attrs={'class':'form-control','placeholder':'YYYY-MM-DD'}),
            'contact_no':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Contact number'}),
            'latitude':forms.NumberInput(attrs={'class':'form-control'}),
            'longitude':forms.NumberInput(attrs={'class':'form-control'}),
            'avatar':forms.FileInput(attrs={'class':'form-control'}),
            'services':forms.SelectMultiple(attrs={'class':'form-select'})
        }
        exclude = ('mechanic',"is_approve","is_busy","is_active")


class HelpForm(forms.ModelForm):
    class Meta:
        model = Help
        fields = ('vehicle_type','service','problem_desc')
        widgets = {
            'vehicle_type':forms.Select(attrs={"class":'form-select','placeholder':'Choose Vehicle type'}),
            'service':forms.Select(attrs={"class":'form-select','placeholder':'Choose Vehicle service'}),
            'problem_desc':forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'write your vehicle problem in detail'}),
            
        }

        
    