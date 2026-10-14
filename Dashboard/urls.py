from django.urls import include, path

from Dashboard import views

urlpatterns = [
    path('', views.lander, name='lander'),
    path('portal/', views.portal, name='portal'),
    path('accounts/', include('Accounts.urls')),
    path('', include('Portfolio.urls')),
]
