from django.urls import path
from django.urls.resolvers import URLPattern
from tracker.views.driver import *
from tracker.views.driver_help import *

urlpatterns = [
    path('',DriverIndexView.as_view(),name="driver_index"),
    path("signup/",DriverSignUpView.as_view(),name="driver_signup"),
    path("login/",DriverLoginView.as_view(),name="driver_login"),
    path("logout/",DriverLogoutView.as_view(),name="driver_logout"),
    path('account/',DriverAccountView.as_view(),name="driver_account"),
    
    path("send-help/",SendHelpView.as_view(),name="send_help"),
    path("send-help-again/",SendHelpRequestAgain.as_view(),name="send_help_again"),
    path("available-mechanics/",available_mechanics,name="available_mechanics"),
    path("fetch-mechanic-data/",FetchMechanicData.as_view()),

]