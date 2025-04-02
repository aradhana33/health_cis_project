# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.dashboard, name='dashboard'),
#     path('api/summary/', views.api_summary, name='api-summary'),
#     path('api/province-stats/', views.api_province_stats, name='api-province-stats'),
# ]

from django.urls import path
from .views import dashboard_from_excel

urlpatterns = [
    path('dashboard/', dashboard_from_excel, name='dashboard_excel'),
    #path('hypothesis1/', hypothesis_one_view, name='hypothesis_one'),
]
