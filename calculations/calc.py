from calculations.FOT import FOT
from calculations.experience import Experience
from calculations.paid import Paid
from db.db import DataBase
import logging

from visualization.visual import Visual

logger = logging.getLogger("MyApp")


class Calc(DataBase, FOT, Experience, Paid, Visual):
    def calculate_from_main(self, limit):
        """
        Функция, которая выполняет весь расчет по лимиту
        и возвращает result_emp (для использования в Django)
        """
        logger.info("Формируется общий датафрейм")

        employees, vacancies = self.create_df()

        result_emp, _ = self.calc_FOT(employees, vacancies)
        result_emp = self.culc_exp(result_emp)
        result_emp = self.calc_paid(result_emp)
        result_emp, stats = self.increase_salary(result_emp, limit)

        self.paid_plt(result_emp)

        return result_emp, stats
