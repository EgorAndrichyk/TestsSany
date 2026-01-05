from calculations.experience import Experience
from calculations.paid import Paid
from db.db import DataBase
from calculations.FOT import FOT
from visualization.visual import Visual


def main():
    db = DataBase()
    employees, vacancies = db.create_df()

    calculation = FOT()
    result_emp, result_vac = calculation.calc_FOT(employees, vacancies)

    exp = Experience()
    result_emp = exp.culc_exp(result_emp)
    limit = int(input("Введите лимит по повышению оплаты: "))

    paid = Paid()
    result_emp = paid.calc_paid(result_emp)
    result_emp = paid.increase_salary(result_emp, limit)

    # result_emp.to_csv("fff.csv", index=False)

    visuals = Visual()
    visuals.paid_plt(result_emp)


if __name__ == "__main__":
    main()
