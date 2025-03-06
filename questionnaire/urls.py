from django.urls import path
from . import views


 
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('pill_intake/', views.pill_intake_view, name='pill_intake'),
    path('symptom_degrees/', views.symptom_degrees_view, name='symptom_degrees'),
    path('tablet_info/', views.tablet_info_view, name='tablet_info'),
    path('thank_you/', views.thank_you_view, name='thank_you'),
]
      

