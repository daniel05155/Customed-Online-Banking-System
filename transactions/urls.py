from django.urls import path
from . import views

urlpatterns = [
    
    path('transactions/deposit/', views.deposit, name ="deposit"),
    path('transactions/withdrawal/', views.withdrawal, name ="withdrawal"),
    path('transactions/transfer/', views.transfer, name ="transfer"),
    path('transactions/report/', views.transaction_report, name ="transaction_report"),
    
]

