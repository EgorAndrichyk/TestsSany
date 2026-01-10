# models.py
from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    tab_number = models.CharField(max_length=20, unique=True, verbose_name="Таб. №")
    is_budgetolog = models.BooleanField(default=False, verbose_name="Бюджетолог")

    def get_full_name(self):
        try:
            person = People.objects.get(tab_number=self.tab_number)
            return person.full_name
        except People.DoesNotExist:
            return "ФИО не найдено"
        
    def __str__(self):
        return (
            f"{self.tab_number} ({'Бюджетолог' if self.is_budgetolog else 'Сотрудник'})"
        )


class People(models.Model):
    tab_number = models.CharField(
        max_length=20, verbose_name="Таб. №", db_column="Таб. №", primary_key=True
    )
    full_name = models.CharField(
        max_length=200, verbose_name="ФИО", db_column="Ф.И.О.", blank=True
    )
    position = models.CharField(
        max_length=200,
        verbose_name="Должность",
        db_column="Должность /профессия (разряд, категория)",
        blank=True,
    )
    recommendation = models.TextField(
        verbose_name="Рекомендация",
        db_column="Рекомендации к повышению оплаты",
        blank=True,
    )
    increase = models.FloatField(
        verbose_name="Повышение", db_column="Повышение оплаты", null=True, blank=True
    )
    fot = models.FloatField(verbose_name="ФОТ", db_column="ФОТ", null=True, blank=True)

    class Meta:
        db_table = "peoples"
        managed = False
