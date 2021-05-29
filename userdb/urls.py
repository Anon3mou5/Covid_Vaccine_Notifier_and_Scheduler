from django.urls import  path
from . import  views

urlpatterns=[
    path('notify/',views.add_user),
    path('zzz/',views.get_user),
]