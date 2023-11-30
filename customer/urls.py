from django.urls import path
from .views import *


urlpatterns = [
    path('productdetails/<int:id>',Productdetailsview.as_view(),name='prodet'),
    path('addtocart/<int:id>',Addtocartview.as_view(),name='acart'),
    path('cartlist',Cartlistview.as_view(),name='cartlist'),
    path('delcart/<int:id>',Deletecartitem.as_view(),name='rcart'),
    path('cout/<int:id>',Checkoutview.as_view(),name='cout'),
    path('order',Orderlistview.as_view(),name='order'),
    path('corder/<int:id>',cancelorder,name='corder'),
    path('addreview/<int:id>',addreview,name='areview'),

] 