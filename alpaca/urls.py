from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name='home'),
    path('CSRF/', views.generateCSRF),
    path('account/', views.AccountInfo.as_view(), name='account'),
    path('positions/', views.Positions.as_view(), name='positions'),
    path('orders/', views.Orders.as_view(), name='orders'),
    path('portfolio/', views.Portfolio.as_view(), name='portfolio'),
    path('activities/', views.Activities.as_view(), name='activities'),
    path('clock/', views.Clock.as_view(), name='clock'),
    path('bars/', views.Bars.as_view(), name='bars'),
]