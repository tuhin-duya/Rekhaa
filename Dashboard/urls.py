"""
URL configuration for Rekhaa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from Dashboard import views
from Portfolio import views as portfolio_views

urlpatterns = [
    path('',views.lander, name='lander'),
    path('accounts/', include('Accounts.urls')),
    # path('customer/', views.customer_dashboard, name='customer_dashboard'),
    # path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('',include('Portfolio.urls')),
    # path('shop/',include('Shop.urls'))    
]

