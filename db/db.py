import pandas as pd
import glob
import os
from constants.constants import PATH


class DataBase:
    """Класс для создания датафрейма."""

    def create_df(self):
        """Метод для создания датафрейма."""

        all_files = glob.glob(os.path.join(PATH, "*.csv"))
        list_of_dataframes = []
        for file in all_files:
            df = pd.read_csv(file, sep="\t", on_bad_lines="skip")
            list_of_dataframes.append(df)

        full_df = pd.concat(list_of_dataframes, axis=0, ignore_index=True)

        vacancy_statuses = ["Вакансия"]
        vacancies = full_df[full_df["Статус назначения"].isin(vacancy_statuses)]
        employees = full_df[~full_df["Статус назначения"].isin(vacancy_statuses)]

        employee_data = employees.groupby("Таб. №").first().reset_index()

        dataframes_by_type = {}
        for df in list_of_dataframes:
            if "Таб. №" in df.columns:
                for col in df.columns:
                    if col != "Таб. №" and col not in dataframes_by_type:
                        dataframes_by_type[col] = df[["Таб. №", col]].dropna()

        merged_employees = employee_data[["Таб. №"]].drop_duplicates()
        for col_name, df_part in dataframes_by_type.items():
            merged_employees = pd.merge(
                merged_employees, df_part, on="Таб. №", how="outer"
            )

        merged_employees = self.apply_fot_and_insurance(merged_employees)

        vacancies = vacancies.drop(
            columns=["ФОТ по рынку", "Процентр страховых взносов"], errors="ignore"
        )

        merged_vacancy = self.apply_fot_and_insurance(vacancies)

        merged_vacancy = (
            merged_vacancy.groupby(["Имя штатной единицы", "Статус назначения"])
            .first()
            .reset_index()
        )

        return merged_employees, merged_vacancy

    def apply_fot_and_insurance(self, df):
        """Применяет объединение с ФОТ и страховыми взносами к переданному датафрейму."""

        fot = pd.read_csv(f"{PATH}/ФОТ по рынку.csv", sep="\t", on_bad_lines="skip")
        key_cols = [
            "Структурное подразделение - полный путь с группирующими",
            "Код функции",
            "Должность /профессия (разряд, категория)",
            "Грейд",
        ]
        fot = fot.drop_duplicates(subset=key_cols)

        df = pd.merge(df, fot, on=key_cols, how="left")

        insurance = pd.read_csv(
            f"{PATH}/Страховые взносы.csv", sep="\t", on_bad_lines="skip"
        )
        insurance = insurance.drop_duplicates(subset=["РФ"])

        df = pd.merge(df, insurance, on=["РФ"], how="left")

        return df
