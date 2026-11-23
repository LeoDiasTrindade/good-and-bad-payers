"""Regras de limpeza derivadas da EDA (notebooks/01_eda.ipynb).

Todas as funções aqui são *sem estado*: cada linha é tratada só com os seus
próprios valores, sem olhar estatísticas da base (média, mediana, quantis...).
Por isso podem rodar antes do split sem causar leakage. Tudo que aprende com os
dados (imputação pela mediana, padronização, o modelo) fica dentro da Pipeline do
scikit-learn, ajustado apenas nos folds de treino.
"""

from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
DADOS_RAW = RAIZ / "data" / "raw"

TARGET_NAME = "SeriousDlqin2yrs"

COLS_ATRASO = [
    "NumberOfTime30-59DaysPastDueNotWorse",
    "NumberOfTime60-89DaysPastDueNotWorse",
    "NumberOfTimes90DaysLate",
]

# Limite de uso do rotativo: acima de 400% do limite tratamos como erro de cadastro
# (decisão da EDA: a contagem de linhas cai de forma gradual a partir de 4).
LIMITE_ROTATIVO = 4

# Códigos 96 e 98 nas colunas de atraso não são contagens reais (saltam de 17 para 96).
CODIGOS_ATRASO_INVALIDOS = [96, 98]

# Features com cauda longa (skew alto na EDA) que recebem log1p no modelo linear.
COLS_CAUDA_LONGA = [
    "RevolvingUtilizationOfUnsecuredLines",
    "DebtRatio",
    "MonthlyIncome",
    "NumberOfOpenCreditLinesAndLoans",
    "NumberRealEstateLoansOrLines",
    "NumberOfDependents",
    *COLS_ATRASO,
]


def carregar_treino(caminho: Path | str | None = None) -> pd.DataFrame:
    """Lê cs-training.csv (150k clientes, 10 features, alvo binário)."""
    caminho = caminho or DADOS_RAW / "cs-training.csv"
    return pd.read_csv(caminho, index_col=0)


def carregar_teste_kaggle(caminho: Path | str | None = None) -> pd.DataFrame:
    """Lê cs-test.csv (sem rótulo; usado só para gerar a submissão do Kaggle)."""
    caminho = caminho or DADOS_RAW / "cs-test.csv"
    return pd.read_csv(caminho, index_col=0)


def criar_indicadores(df: pd.DataFrame) -> pd.DataFrame:
    """Sinaliza a origem de cada valor faltante/inválido antes de anulá-lo.

    - Missing-MonthlyIncome: renda não informada. Nesses casos o DebtRatio também
      é inválido (na EDA, 89% de correlação entre DebtRatio > 10 e renda faltante).
    - Missing-NumberOfDependents: sempre ocorre junto com renda faltante.
    - Atraso-codigo-invalido: códigos 96/98 nas colunas de atraso (ocorrem nas três
      colunas ao mesmo tempo, então um indicador basta).
    - Rotativo-invalido: uso do rotativo acima de 400%.
    """
    df = df.copy()
    df["Missing-MonthlyIncome"] = df["MonthlyIncome"].isna().astype(int)
    df["Missing-NumberOfDependents"] = df["NumberOfDependents"].isna().astype(int)
    df["Atraso-codigo-invalido"] = (
        df[COLS_ATRASO].isin(CODIGOS_ATRASO_INVALIDOS).any(axis=1).astype(int)
    )
    df["Rotativo-invalido"] = (
        df["RevolvingUtilizationOfUnsecuredLines"] > LIMITE_ROTATIVO
    ).astype(int)
    return df


def limpar_sujeiras(df: pd.DataFrame) -> pd.DataFrame:
    """Anula valores impossíveis encontrados na EDA (viram NaN e são imputados depois)."""
    df = df.copy()
    df.loc[df["age"] == 0, "age"] = np.nan
    df.loc[
        df["RevolvingUtilizationOfUnsecuredLines"] > LIMITE_ROTATIVO,
        "RevolvingUtilizationOfUnsecuredLines",
    ] = np.nan
    for col in COLS_ATRASO:
        df.loc[df[col].isin(CODIGOS_ATRASO_INVALIDOS), col] = np.nan
    df.loc[df["MonthlyIncome"].isna(), "DebtRatio"] = np.nan
    return df


def preparar_features(df: pd.DataFrame) -> pd.DataFrame:
    """Indicadores + limpeza. Remove o alvo, se presente. Sem estado (não aprende nada)."""
    df = df.drop(columns=[TARGET_NAME], errors="ignore")
    return limpar_sujeiras(criar_indicadores(df))


def log_cauda_longa(df: pd.DataFrame) -> pd.DataFrame:
    """log(1 + x) nas features de cauda longa; NaN continua NaN. Sem estado."""
    df = df.copy()
    df[COLS_CAUDA_LONGA] = np.log1p(df[COLS_CAUDA_LONGA])
    return df
