from django.urls import path
from .views import alibaba

urlpatterns = [
    path('alibaba/', alibaba, name='alibaba'),
]
