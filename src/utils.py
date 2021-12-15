from typing import Optional, Tuple

import fiona
import geopandas as gpd
import requests
from catboost import CatBoostClassifier
from lightgbm import Booster

from src.constants import (CATBOOST_PATH, DATA_LINKS, FEATURES, LIGHTGBM_PATH,
                           PROBABILITY_THRESHOLD)


def init_models() -> Tuple[CatBoostClassifier, Booster]:
    model_cbc = CatBoostClassifier()
    model_cbc.load_model(CATBOOST_PATH)

    model_lgb = Booster(model_file=LIGHTGBM_PATH)

    return model_cbc, model_lgb


def update_data() -> None:
    gpd_data: Optional[gpd.GeoDataFrame] = None
    for link in DATA_LINKS:
        response = requests.get(link)
        if response.status_code == 200:
            with fiona.BytesCollection(response.content) as b:
                if gpd_data is None:
                    gpd_data = gpd.GeoDataFrame.from_features(b)
                else:
                    gpd_data = gpd_data.append(
                        gpd.GeoDataFrame.from_features(b),
                    )

    df = gpd_data.rename(columns={'BRIGHT_TI4': 'BRIGHTNESS', 'BRIGHT_TI5': 'BRIGHT_T31'})
    df = df[FEATURES].copy()
    df['CONFIDENCE'] = df['CONFIDENCE'].map({'l': 0, 'h': 1, 'n': 3})
    df['SATELLITE'] = df['SATELLITE'].map({'1': 0, 'N': 1})
    df['DAYNIGHT'] = df['DAYNIGHT'].map({'D': 0, 'N': 1})
    df['ACQ_TIME'] = df['ACQ_TIME'].astype(int)

    return df


def predict_fires(model_cbc, model_lgb, df):
    preds_cbc = model_cbc.predict_proba(df)
    preds_lgb = model_lgb.predict(df)

    preds = (preds_cbc[:, 1] + preds_lgb) / 2

    df['predict_proba'] = preds
    filtered_df = df[df['predict_proba'] > PROBABILITY_THRESHOLD]

    return filtered_df
