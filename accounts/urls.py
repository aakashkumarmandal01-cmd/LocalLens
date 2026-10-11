from django.urls import path
from django.contrib.auth.views import LogoutView,PasswordResetView,PasswordResetDoneView
from .views import register,LocalLoginView
urlpatterns=[path('register/',register,name='register'),path('login/',LocalLoginView.as_view(),name='login'),path('logout/',LogoutView.as_view(),name='logout'),path('password-reset/',PasswordResetView.as_view(template_name='accounts/password_reset.html'),name='password_reset'),path('password-reset/done/',PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_done')]
