# admin.py
from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("tab_number", "is_budgetolog", "user")
    search_fields = ("tab_number",)
    list_filter = ("is_budgetolog",)
