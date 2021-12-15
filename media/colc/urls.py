from django.urls import path

from .views import loginuser,logoutuser,registration,change_password,profile
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView


urlpatterns = [
    path('login/',loginuser,name="login"),
    path('logout/',logoutuser,name="logout"),
    path('singup/',registration,name="singup"),
    path('password/',change_password,name="password"),
    path('profile/',profile,name="profile"),
    
    
    
    
    path('reset/password/',PasswordResetView.as_view(template_name='now/reset_pass.html'),name="password_reset"),
    path('reset/password/done/',PasswordResetDoneView.as_view(template_name='now/reset_pass_done.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>',PasswordResetConfirmView.as_view(template_name='now/password_reset_confirm.html'),name="password_reset_confirm"),
    path('reset/done/',PasswordResetCompleteView.as_view(template_name='now/password_reset_complete.html'),name="password_reset_complete"),
    
]
