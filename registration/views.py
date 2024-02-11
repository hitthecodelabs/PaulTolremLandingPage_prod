from .forms import UserRegisterForm
from .forms import UserRegistrationForm
from .models import UserProfile, ActivityLog

from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
# from django.core.management import call_command

from rest_framework.authtoken.models import Token
# Use your custom user model instead of Django's built-in one
from registration.models import User  


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()

            # Crear perfil de usuario y guardar el número de teléfono
            user_profile = UserProfile(
                user=new_user,
                first_name=user_form.cleaned_data['first_name'],
                middle_name=user_form.cleaned_data['middle_name'],
                last_name=user_form.cleaned_data['last_name'],
                phone_number=user_form.cleaned_data['phone_number'],
            )
            user_profile.save()
    
            # Registrar la actividad de registro
            activity_log = ActivityLog(user=new_user, action="Sign in")
            activity_log.save()

            # Iniciar sesión automáticamente después del registro
            login(request, new_user)

            return HttpResponseRedirect(reverse('home'))
    else:
        user_form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': user_form})

def register_0(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # Crear perfil de usuario y guardar el número de teléfono
            user_profile = UserProfile(user=new_user, phone_number=user_form.cleaned_data['phone_number'])
            user_profile.save()
    
            # Registrar la actividad de registro
            activity_log = ActivityLog(user=new_user, action="Sign in")
            activity_log.save()

            # Iniciar sesión automáticamente después del registro
            login(request, new_user)

            return HttpResponseRedirect(reverse('home'))
    else:
        user_form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Registrar la actividad de inicio de sesión
            activity_log = ActivityLog(user=user, action="Log in")
            activity_log.save()

            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    # Registrar la actividad de cierre de sesión
    activity_log = ActivityLog(user=request.user, action="Logout")
    activity_log.save()

    logout(request)
    return redirect('login')

# @login_required
def home(request):
    return render(request, 'registration/home.html')


'''
class TokenCreationView(View):
    def get(self, request, *args, **kwargs):
        User = get_user_model()
        users = User.objects.all()

        for user in users:
            Token.objects.get_or_create(user=user)
        
        return HttpResponse('Tokens created for all users.', status=200)

class CreateSuperuserView(View):
    def get(self, request):
        User.objects.create_superuser('odin', 'jpaul@paultolrem.com', 'Ojo Arranco .25')
        return HttpResponse("Superuser created.")


class MakeSuperuserView(View):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)  # Query your custom user model
            user.is_superuser = True
            user.is_staff = True
            user.save()
            return HttpResponse(f"User {username} is now a superuser.")
        except User.DoesNotExist:
            return HttpResponse("User not found.")
'''