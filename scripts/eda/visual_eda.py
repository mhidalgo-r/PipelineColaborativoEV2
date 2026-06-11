import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# ==========================
# CREAR CARPETAS
# ==========================
os.makedirs("reports/figures", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# ==========================
# LOGGER
# ==========================
logging.basicConfig(
    filename="logs/visual_eda.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)
logger = logging.getLogger()

# ==========================
# ARCHIVO
# ==========================
INPUT_FILE = "data/processed/bank_cleaned.csv"


# ==========================
# UNIVARIADO: EDAD
# ==========================
def age_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df["age"], bins=20, kde=True, color="steelblue")
    plt.title("Distribución de Edad de Clientes", fontsize=14, fontweight="bold")
    plt.xlabel("Edad (años)", fontsize=12)
    plt.ylabel("Cantidad de Clientes", fontsize=12)
    mean_age = df["age"].mean()
    plt.axvline(mean_age, color="red", linestyle="--", label=f"Promedio: {mean_age:.1f} años")
    plt.legend(fontsize=11)
    plt.figtext(
        0.5, -0.02,
        "Análisis univariado: muestra cómo se distribuyen las edades de los clientes del banco.\n"
        "La línea roja indica la edad promedio.",
        wrap=True, horizontalalignment="center", fontsize=10, color="gray"
    )
    plt.tight_layout()
    plt.savefig("reports/figures/hist_age.png", bbox_inches="tight")
    plt.close()


# ==========================
# UNIVARIADO: BALANCE
# ==========================
def balance_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df["balance"], bins=20, kde=True, color="coral")
    plt.title("Distribución del Balance de Cuenta", fontsize=14, fontweight="bold")
    plt.xlabel("Balance (euros)", fontsize=12)
    plt.ylabel("Cantidad de Clientes", fontsize=12)
    mean_bal = df["balance"].mean()
    plt.axvline(mean_bal, color="darkred", linestyle="--", label=f"Promedio: {mean_bal:.0f} €")
    plt.legend(fontsize=11)
    plt.figtext(
        0.5, -0.02,
        "Análisis univariado: muestra cómo se distribuye el saldo bancario de los clientes.\n"
        "La mayoría de clientes tiene balances bajos, con pocos casos de balances muy altos.",
        wrap=True, horizontalalignment="center", fontsize=10, color="gray"
    )
    plt.tight_layout()
    plt.savefig("reports/figures/balance_distribution.png", bbox_inches="tight")
    plt.close()


# ==========================
# UNIVARIADO: DURACION
# ==========================
def duration_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df["duration"], bins=20, kde=True, color="mediumseagreen")
    plt.title("Distribución de Duración de Llamada", fontsize=14, fontweight="bold")
    plt.xlabel("Duración (segundos)", fontsize=12)
    plt.ylabel("Cantidad de Llamadas", fontsize=12)
    mean_dur = df["duration"].mean()
    plt.axvline(mean_dur, color="darkgreen", linestyle="--", label=f"Promedio: {mean_dur:.0f} seg")
    plt.legend(fontsize=11)
    plt.figtext(
        0.5, -0.02,
        "Análisis univariado: duración de cada llamada de campaña.\n"
        "Es una variable clave: llamadas más largas tienden a resultar en depósitos.",
        wrap=True, horizontalalignment="center", fontsize=10, color="gray"
    )
    plt.tight_layout()
    plt.savefig("reports/figures/duration_distribution.png", bbox_inches="tight")
    plt.close()


# ==========================
# UNIVARIADO: DEPOSITO
# ==========================
def deposit_analysis(df):
    counts = df["deposit"].value_counts()
    colores = ["steelblue", "coral"]
    plt.figure(figsize=(7, 7))
    wedges, texts, autotexts = plt.pie(
        counts,
        labels=["No depositó", "Sí depositó"],
        autopct="%1.1f%%",
        colors=colores,
        startangle=90
    )
    for text in autotexts:
        text.set_fontsize(12)
        text.set_fontweight("bold")
    plt.title(
        "Distribución de Clientes según Depósito\n(Variable Objetivo)",
        fontsize=14, fontweight="bold"
    )
    plt.figtext(
        0.5, -0.02,
        "Análisis univariado: proporción de clientes que realizaron o no un depósito.\n"
        "Esta es la variable que el modelo de IA aprende a predecir.",
        wrap=True, horizontalalignment="center", fontsize=10, color="gray"
    )
    plt.tight_layout()
    plt.savefig("reports/figures/deposit_analysis.png", bbox_inches="tight")
    plt.close()


# ==========================
# BIVARIADO: BALANCE VS DEPOSITO
# ==========================
def balance_vs_deposit(df):
    plt.figure(figsize=(9, 6))
    ax = sns.boxplot(
        x="deposit",
        y="balance",
        data=df,
        hue="deposit",
        palette={"yes": "steelblue", "no": "coral"},
        legend=False
    )
    plt.title(
        "Balance de Cuenta según si el Cliente Depositó o No",
        fontsize=14, fontweight="bold"
    )
    plt.xlabel("¿Realizó depósito?  (no = No  |  yes = Sí)", fontsize=12)
    plt.ylabel("Balance de cuenta (euros)", fontsize=12)

    # Mediana de cada grupo
    medians = df.groupby("deposit")["balance"].median()
    for i, (grupo, mediana) in enumerate(medians.items()):
        ax.text(
            i, mediana + 50,
            f"Mediana: {mediana:.0f}€",
            ha="center", fontsize=10, color="black", fontweight="bold"
        )

    plt.figtext(
        0.5, -0.04,
        "Análisis bivariado: compara el balance bancario entre clientes que depositaron y los que no.\n"
        "Si la caja azul (Sí) está más alta, los clientes con más saldo tienden a depositar más.",
        wrap=True, horizontalalignment="center", fontsize=10, color="gray"
    )
    plt.tight_layout()
    plt.savefig("reports/figures/balance_vs_deposit.png", bbox_inches="tight")
    plt.close()


# ==========================
# BIVARIADO: EDAD VS DEPOSITO
# ==========================
def age_vs_deposit(df):
    plt.figure(figsize=(9, 6))
    ax = sns.boxplot(
        x="deposit",
        y="age",
        data=df,
        hue="deposit",
        palette={"yes": "steelblue", "no": "coral"},
        legend=False
    )
    plt.title(
        "Edad del Cliente según si Realizó Depósito o No",
        fontsize=14, fontweight="bold"
    )
    plt.xlabel("¿Realizó depósito?  (no = No  |  yes = Sí)", fontsize=12)
    plt.ylabel("Edad del cliente (años)", fontsize=12)

    medians = df.groupby("deposit")["age"].median()
    for i, (grupo, mediana) in enumerate(medians.items()):
        ax.text(
            i, mediana + 0.5,
            f"Mediana: {mediana:.0f} años",
            ha="center", fontsize=10, color="black", fontweight="bold"
        )

    plt.figtext(
        0.5, -0.04,
        "Análisis bivariado: compara la edad entre clientes que depositaron y los que no.\n"
        "La caja azul (Sí) muestra el rango de edades de quienes sí depositaron.\n"
        "Si ambas cajas son similares, la edad sola no determina si un cliente deposita.",
        wrap=True, horizontalalignment="center", fontsize=10, color="gray"
    )
    plt.tight_layout()
    plt.savefig("reports/figures/age_vs_deposit.png", bbox_inches="tight")
    plt.close()


# ==========================
# CORRELACION
# ==========================
def correlation(df):
    numeric = df.select_dtypes(include=["number"])
    corr = numeric.corr()
    plt.figure(figsize=(11, 9))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        linewidths=0.5,
        annot_kws={"size": 9}
    )
    plt.title(
        "Matriz de Correlación entre Variables Numéricas",
        fontsize=14, fontweight="bold"
    )
    plt.figtext(
        0.5, -0.02,
        "Valores cercanos a 1 o -1 indican correlación fuerte entre variables.\n"
        "Valores cercanos a 0 indican que las variables son independientes entre sí.",
        wrap=True, horizontalalignment="center", fontsize=10, color="gray"
    )
    plt.tight_layout()
    plt.savefig("reports/figures/correlation.png", bbox_inches="tight")
    plt.close()


# ==========================
# MAIN
# ==========================
def execute_eda():
    logger.info("=" * 50)
    logger.info("INICIO EDA VISUAL")
    logger.info("=" * 50)

    try:
        df = pd.read_csv(INPUT_FILE)
        logger.info(f"Dataset cargado: {df.shape[0]} filas")

        age_distribution(df)
        logger.info("Histograma edad OK")

        balance_distribution(df)
        logger.info("Histograma balance OK")

        duration_distribution(df)
        logger.info("Histograma duracion OK")

        deposit_analysis(df)
        logger.info("Grafico deposito OK")

        balance_vs_deposit(df)
        logger.info("Bivariado balance vs deposito OK")

        age_vs_deposit(df)
        logger.info("Bivariado edad vs deposito OK")

        correlation(df)
        logger.info("Matriz correlacion OK")

        print("\nGráficos generados correctamente en:")
        print("  reports/figures/")

    except Exception as e:
        logger.error(f"ERROR: {str(e)}")
        print(e)


if __name__ == "__main__":
    execute_eda()