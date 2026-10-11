from django.urls import path
from . import views
urlpatterns=[path('',views.home,name='home'),path('places/',views.place_list,name='place_list'),path('places/saved/',views.saved_places,name='saved_places'),path('places/<slug:slug>/',views.place_detail,name='place_detail'),path('places/<slug:slug>/save/',views.toggle_saved,name='toggle_saved')]
