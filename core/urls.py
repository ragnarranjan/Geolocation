from django.urls import path
from . import views

urlpatterns = [
    path('getAddressDetails', views.AddressDetail.as_view(), name='AddressDetail'),
]