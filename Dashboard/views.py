from django.shortcuts import render

# Create your views here.

def lander(request):
    return render(request, 'dashboard/lander.html')

def customer_dashboard(request):
    return render(request, 'dashboard/customer_dashboard.html')

def manager_dashboard(request):
    return render(request, 'dashboard/manager_dashboard.html')