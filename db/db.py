import sqlite3
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

        full_df = list_of_dataframes[0]
        for df in list_of_dataframes[1:]:
            full_df = pd.merge(full_df, df, how='inner')

        vacancy_statuses = ["Вакансия"]
        vacancies = full_df[full_df["Статус назначения"].isin(vacancy_statuses)]
        employees = full_df[~full_df["Статус назначения"].isin(vacancy_statuses)]

        merged_employees = employees.drop_duplicates(subset="Имя штатной единицы")

        merged_vacancy = (
            vacancies.groupby(["Имя штатной единицы", "Статус назначения"])
            .first()
            .reset_index()
        )

        return merged_employees, merged_vacancy

    def df_from_db(self, db: pd.DataFrame):
        conn = sqlite3.connect("db.sqlite3")
        db.to_sql("peoples", conn, if_exists="replace", index=False)
        conn.close()
