from django.urls import path
from .views import *


urlpatterns = [
    path('reg',Regview.as_view(),name='reg'),
    path('home',Homeview.as_view(),name='home'),
    path('lgout',Lgoutview.as_view(),name='logout')

]