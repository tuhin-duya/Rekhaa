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
from Portfolio import views 

urlpatterns = [
    path('about/',views.about,name="about"),
    path('about/edit/',views.edit_about,name="edit_about"),
    path('category/',views.art_category,name="category"),
    path('category/<int:pk>/',views.category_detail,name="category_detail"),
    path('add_category/',views.add_category,name="add_category"),
    path('category/<int:category_id>/add_painting/', views.add_painting, name="add_painting"),
    path('painting/<int:pk>/delete/', views.del_painting, name="delete_painting"),
    path('painting/<int:pk>/edit/',views.edit_painting,name="edit_painting"),
    path('category/<int:pk>/delete/',views.del_category,name="delete_category"),
    path('category/<int:pk>/edit/',views.edit_category,name="edit_category"),
]

