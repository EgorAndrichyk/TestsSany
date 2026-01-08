from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Employee, People
from calculations.calc import Calc
from users.utils import generate_password


class RunMainView(View):
    """Запуск подготовки БД."""

    def get(self, request: HttpRequest):
        return render(request, "run_main.html")

    def post(self, request: HttpRequest):
        limit = request.POST.get("limit", "10000000")
        try:
            limit = int(limit)
        except ValueError:
            return JsonResponse({"error": "Лимит должен быть числом"}, status=400)

        calc = Calc()
        result_emp, _ = calc.calculate_from_main(limit)
        calc.df_from_db(result_emp)

        messages.success(request, "Данные успешно загружены!")
        return redirect("register")


class RegisterView(View):
    """Регистрация пользователя."""

    def get(self, request: HttpRequest):
        return render(request, "register.html")

    def post(self, request: HttpRequest):
        tab_number = request.POST.get("tab_number")
        is_budgetolog = request.POST.get("is_budgetolog", False)

        if not tab_number:
            messages.error(request, "Табельный номер обязателен")
            return render(request, "register.html")

        if Employee.objects.filter(tab_number=tab_number).exists():
            messages.error(request, "Этот табельный номер уже зарегистрирован")
            return render(request, "register.html")

        try:
            _ = People.objects.get(tab_number=tab_number)
        except People.DoesNotExist:
            messages.error(request, "Такого табельного номера нет в базе")
            return render(request, "register.html")

        password = generate_password()
        user = User.objects.create_user(
            username=tab_number,
            password=password
        )

        _ = Employee.objects.create(
            user=user,
            tab_number=tab_number,
            is_budgetolog=is_budgetolog == 'on'
        )

        messages.success(request, f"Регистрация успешна! Логин: {tab_number}, Пароль: {password}")
        return redirect('login')


class LoginView(View):
    """Вход пользователя."""

    def get(self, request: HttpRequest):
        return render(request, "login.html")

    def post(self, request: HttpRequest):
        tab_number = request.POST.get("tab_number")
        password = request.POST.get("password")

        user = authenticate(request, username=tab_number, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Неверный табельный номер или пароль")

        return render(request, "login.html")


class DashboardView(LoginRequiredMixin, View):
    """Личный кабинет пользователя."""

    def get(self, request: HttpRequest):
        employee = Employee.objects.get(user=request.user)

        try:
            person = People.objects.get(tab_number=employee.tab_number)
            position = person.position
            fot = person.fot
            full_name = person.full_name
        except People.DoesNotExist:
            position = fot = full_name = "Не найдено"

        context = {
            "employee": employee,
            "full_name": full_name,
            "position": position,
            "fot": fot,
        }
        return render(request, "dashboard.html", context)


class BudgetologDashboardView(LoginRequiredMixin, View):
    """Страница бюджетолога."""

    def get(self, request: HttpRequest):
        employee = Employee.objects.get(user=request.user)
        if not employee.is_budgetolog:
            messages.error(request, "У вас нет прав бюджетолога")
            return redirect('dashboard')

        calc_stats = request.session.get('calc_stats', {})

        calc_result = list(
            People.objects.filter(
                Q(recommendation="Рекомендуется") &
                Q(increase__isnull=False)
            )
            .values('tab_number', 'full_name', 'position', 'recommendation', 'increase')
            .order_by('?')[:100]
        )

        paginator = Paginator(calc_result, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'employee': employee,
            'page_obj': page_obj,
            'limit': request.POST.get('limit', '10000000'),
            'stats': calc_stats,
            'graph_mrf_url': '/static/images/graph_mrf.png',
            'graph_grade_url': '/static/images/graph_grade.png',
        }
        return render(request, 'budgetolog.html', context)

    def post(self, request: HttpRequest):
        employee = Employee.objects.get(user=request.user)
        if not employee.is_budgetolog:
            messages.error(request, "У вас нет прав бюджетолога")
            return redirect('dashboard')

        limit = request.POST.get('limit', '10000000')
        try:
            limit = int(limit)
        except ValueError:
            messages.error(request, "Лимит должен быть числом")
            return render(request, 'budgetolog.html', {'limit': limit})

        try:
            calc = Calc()
            result_emp, stats = calc.calculate_from_main(limit)
            calc.df_from_db(result_emp)

            request.session['calc_stats'] = stats

            messages.success(request, "Расчет выполнен!")
        except Exception as e:
            messages.error(request, f"Ошибка при расчете: {str(e)}")
            return render(request, 'budgetolog.html', {'limit': limit})

        return self.get(request)


class LogoutView(View):
    """Выход из аккаунта пользователя."""

    def get(self, request: HttpRequest):
        logout(request)
        return redirect("login")