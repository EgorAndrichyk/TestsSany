from calculations.experience import Experience
from calculations.paid import Paid
from db.db import DataBase
from calculations.FOT import FOT
from visualization.visual import Visual
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('MyApp')

def calculate_from_main(limit):
    """
    Функция, которая выполняет весь расчет по лимиту
    и возвращает result_emp (для использования в Django)
    """
    logger.info('Формируется общий датафрейм')

    db = DataBase()
    employees, vacancies = db.create_df()

    calculation = FOT()
    result_emp, _ = calculation.calc_FOT(employees, vacancies)

    exp = Experience()
    result_emp = exp.culc_exp(result_emp)

    paid = Paid()
    result_emp = paid.calc_paid(result_emp)
    result_emp = paid.increase_salary(result_emp, limit)

    # result_emp.to_csv("fff.csv", index=False) # Саня посмотри файл

    # Визуализация (опционально — можно вызывать отдельно)
    visuals = Visual()
    visuals.paid_plt(result_emp)

    return result_emp

def main():
    limit = int(input("Введите лимит по повышению оплаты: "))
    result_emp = calculate_from_main(limit)
    logger.info(f"Расчет завершён. Результат содержит {len(result_emp)} строк.")

if __name__ == "__main__":
    main()