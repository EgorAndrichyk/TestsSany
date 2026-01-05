from constants.constants import FORMAT_DATA, TODAY
import pandas as pd


class Experience:
    """Класс для расчета стажа."""

    def culc_exp(self, emp_df):
        """Метод для расчета стажа."""
        emp_df["Дата приема"] = pd.to_datetime(
            emp_df["Дата приема"], format=FORMAT_DATA, errors="coerce"
        )

        emp_df["Стаж"] = (
            ((pd.Timestamp(TODAY) - emp_df["Дата приема"]).dt.days + 1) / 365
        ).round(1)
        return emp_df
