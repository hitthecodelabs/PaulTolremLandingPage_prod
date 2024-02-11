from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    path('how_to_use/', views.how_to_use, name='how_to_use'),
    path('about_us/', views.about_us, name='about_us'),
    path('team/', views.team, name='team'),
]