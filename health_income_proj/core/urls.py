# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.dashboard, name='dashboard'),
#     path('api/summary/', views.api_summary, name='api-summary'),
#     path('api/province-stats/', views.api_province_stats, name='api-province-stats'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_from_excel, name='dashboard_excel'),
    #path('hypothesis1/', hypothesis_one_view, name='hypothesis_one'),
    path('api/gender-pay-gap/', views.api_gender_pay_gap),
    path('api/province-income-health/', views.api_province_income_health),
    path('api/work-mental/', views.api_work_vs_mental),
    path('api/assistance-food/', views.api_assistance_vs_food),
]
