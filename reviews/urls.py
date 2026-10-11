from django.urls import path
from .views import submit_review
urlpatterns=[path('<slug:slug>/submit/',submit_review,name='submit_review')]
