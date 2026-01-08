from django.urls import path
from .views import (
    RunMainView,
    RegisterView,
    LoginView,
    DashboardView,
    BudgetologDashboardView,
    LogoutView,
)

urlpatterns = [
    path('', RunMainView.as_view(), name='home'),
    path('run-main/', RunMainView.as_view(), name='run_main'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('budgetolog/', BudgetologDashboardView.as_view(), name='budgetolog'),
    path('logout/', LogoutView.as_view(), name='logout'),
]