from django.urls import path

from tracker.views.mechanic import *

urlpatterns = [
    path('',MechanicIndexView.as_view(),name="mechanic_index"),
    path("signup/",MechanicSignUpView.as_view(),name="mechanic_signup"),
    path("login/",MechanicLoginView.as_view(),name="mechanic_login"),
    path("logout/",MechanicLogoutView.as_view(),name="mechanic_logout"),
    path("initial-update/",MechanicInitialUpdate.as_view(),name="mechanic_initial_update"),
    path("send-response/",SendResponseView.as_view()),
    path("account/",MechanicAccountView.as_view(),name="mechanic_account")
]