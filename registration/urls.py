from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path('logout/', views.user_logout, name='logout'),
    
    # path('createsuperuser/', views.CreateSuperuserView.as_view(), name='create_superuser'),
    # path('makesuperuser/<str:username>/', views.MakeSuperuserView.as_view(), name='make_superuser'),
    # path('create_tokens/', views.TokenCreationView.as_view(), name='create_tokens'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name='password_reset_complete'),
    
]
