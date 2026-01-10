from calculations.calc import Calc
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("MyApp")


def main():
    limit = int(input("Введите лимит по повышению оплаты: "))
    calc = Calc()
    result_emp, _ = calc.calculate_from_main(limit)
    calc.df_from_db(result_emp)
    
    logger.info(f"Расчет завершён. Результат содержит {len(result_emp)} строк.")


if __name__ == "__main__":
    main()
