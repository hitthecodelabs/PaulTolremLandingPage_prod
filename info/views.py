from django.shortcuts import render

def how_to_use(request):
    return render(request, 'info/how_to_use.html')

def about_us(request):
    return render(request, 'info/about_us.html')

def team(request):
    return render(request, 'info/team.html')