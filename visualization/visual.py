import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd

class Visual:
    """Класс для визуализации графиков."""

    def paid_plt(self, df_emp: pd.DataFrame):
        """Метод для визуализации графиков."""

        mrf = (
            df_emp.dropna(subset=["МРФ", "Повышение оплаты"])
            .groupby("МРФ")["Повышение оплаты"]
            .sum()
            .round(2)
            .reset_index()
        )
        grid = (
            df_emp.dropna(subset=["Грейд", "Повышение оплаты"])
            .groupby("Грейд")["Повышение оплаты"]
            .sum()
            .round(2)
            .reset_index()
        )

        mrf["МРФ"] = (
            mrf["МРФ"]
            .str.extract(r'(".*?")')[0]
            .fillna(mrf["МРФ"])
            .str.replace('"', "")
            .str.strip()
        )

        def thousands_formatter(x, pos):
            return f"{int(x):,}".replace(",", " ")

        plt.figure(figsize=(10, 6))
        plt.bar(x=mrf["МРФ"], height=mrf["Повышение оплаты"])
        plt.xlabel("МРФ")
        plt.ylabel("Повышение оплаты")
        plt.title("График повышения оплаты по МРФ")
        plt.xticks(rotation=45, ha="right")
        plt.gca().yaxis.set_major_formatter(FuncFormatter(thousands_formatter))
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig("static/images/graph_mrf.png")
        plt.close()

        plt.figure(figsize=(8, 6))
        plt.bar(x=grid["Грейд"], height=grid["Повышение оплаты"])
        plt.xlabel("Грейд")
        plt.ylabel("Повышение оплаты")
        plt.title("График повышения оплаты по грейдам")
        plt.gca().yaxis.set_major_formatter(FuncFormatter(thousands_formatter))
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig("static/images/graph_grade.png")
        plt.close()