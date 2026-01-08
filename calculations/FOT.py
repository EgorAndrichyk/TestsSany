import pandas as pd


class FOT:
    """Класс для расчетов ФОТ."""

    def calc_FOT(self, emp_df: pd.DataFrame, vac_df: pd.DataFrame):
        """Расчет ФОТ."""

        def process_df(df: pd.DataFrame):
            """Функция для расширения датафрейма."""

            df["Процент премирования"] = (
                1
                + (
                    df["Процент месячной премии"] * (11 / 12)
                    + df["Процент квартальной премии"] * (9 / 12)
                    + df["Процент годовой премии"]
                )
                / 100
            )
            dop_cols = [
                col
                for col in df.columns
                if any(
                    word in col
                    for word in ["Доплат", "Надбавк", "Выплат", "Ежемесячная"]
                )
            ]
            df["Сумма доплат"] = df[dop_cols].sum(axis=1)
            df["ФОТ"] = (df["Тарифная ставка (оклад), руб."] + df["Сумма доплат"]) * df[
                "Процент премирования"
            ]
            df["ФОТ OPEX"] = df["ФОТ"] * df["OPEX"]
            df["ФОТ CAPEX"] = df["ФОТ"] * df["CAPEX"]
            df["ФОТ с СВ"] = df["ФОТ"] * (1 + df["Процентр страховых взносов"])
            return df

        emp_result = process_df(emp_df)
        vac_result = process_df(vac_df)

        return emp_result, vac_result
