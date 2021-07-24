from django.urls import path,include
from .views import *

urlpatterns = [
    path('driver/',include('tracker.nested_urls.driver')),
    path("mechanic/",include("tracker.nested_urls.mechanic")),
    path('feedback/',FeedbackView.as_view()),
]
