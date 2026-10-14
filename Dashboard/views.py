from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Portfolio.models import Category, Painting


def lander(request):
    return render(request, 'dashboard/lander.html')


@login_required
def portal(request):
    categories = Category.objects.order_by('title')
    return render(request, 'dashboard/portal.html', {
        'categories': categories,
        'category_count': categories.count(),
        'painting_count': Painting.objects.count(),
    })


def customer_dashboard(request):
    return render(request, 'dashboard/customer_dashboard.html')


def manager_dashboard(request):
    return render(request, 'dashboard/manager_dashboard.html')
