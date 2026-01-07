from datetime import timedelta
from constants.constants import FORMAT_DATA, TODAY
import pandas as pd
import logging

logger = logging.getLogger('MyApp')

class Paid:
    """Класс для расчетов повышения оплаты."""

    def calc_paid(self, df_emp: pd.DataFrame):
        """Класс для расчетов проплаченности."""

        df_emp["Проплаченность"] = df_emp["ФОТ"] / df_emp["ФОТ по рынку"]
        df_emp["Проплаченность"] = df_emp["Проплаченность"].fillna(0)

        six_month = (
            pd.Timestamp(pd.to_datetime(TODAY, format=FORMAT_DATA))
            - timedelta(days=180)
        ).date()
        
        df_emp["Дата последнего повышения"] = pd.to_datetime(
            df_emp["Дата последнего повышения"], 
            format="%Y-%m-%d", 
            errors='coerce' 
        )
        
        def safe_date(x):
            if pd.isna(x):
                return None
            return x.date()
        
        df_emp["Дата последнего повышения"] = df_emp["Дата последнего повышения"].apply(safe_date)
        
        valid_dates_mask = df_emp["Дата последнего повышения"].notna()
        
        mask = (
            (df_emp["Проплаченность"] < 0.8)
            & valid_dates_mask 
            & (df_emp["Дата последнего повышения"] < six_month)
            & (df_emp["Стаж"] > 1)
            & (df_emp["Кол-во единиц"] > 0.5)
        )

        df_emp.loc[mask, "Рекомендации к повышению оплаты"] = "Рекомендуется"
        df_emp.loc[~mask, "Рекомендации к повышению оплаты"] = "Не рекомендуется"

        return df_emp

    def increase_salary(self, df_emp: pd.DataFrame, limit: int):
        """Метод для расчетов повышения оплаты."""

        mask = df_emp["Рекомендации к повышению оплаты"] == "Рекомендуется"

        df_emp.loc[mask, "Повышение оплаты"] = (
            df_emp["Тарифная ставка (оклад), руб."] / 100 * 30
        ).round(2)
        df_emp.loc[~mask, "Повышение оплаты"] = 0

        if df_emp["Повышение оплаты"].sum() > limit:
            logger.info(f"Лимит превышен на {(df_emp['Повышение оплаты'].sum() - limit):.2f}, уменьшаем оплату пропорционально")

            percent = (
                (df_emp["Повышение оплаты"].sum() - limit)
                / df_emp["Повышение оплаты"].sum()
                * 100
            )
            df_emp["Повышение оплаты"] = df_emp["Повышение оплаты"] - (
                df_emp["Повышение оплаты"] / 100 * percent
            )

        else:
            logger.info(
                f"Остаток лимита: {(limit - df_emp['Повышение оплаты'].sum()):.2f}"
            )
        logger.info(f"Сумма повышений составила: {df_emp['Повышение оплаты'].sum()}")
        return df_emp
