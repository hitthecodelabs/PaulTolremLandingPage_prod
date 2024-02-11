from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('registration.urls')),
    path('', include('pricing.urls')),
    path('', include('charts.urls')),
    path('', include('info.urls')),
]


'''
urlpatterns = [
    path('', user_views.landing_page, name='landing_page'),  # Add this line
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('home/', user_views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    # ... (rest of the URL patterns)
]
'''
