import pickle
from typing import Any, Callable, Optional, Tuple

import fiona
import geopandas as gpd
import pandas as pd
import pyproj
import requests
import shap
from shapely.geometry import Point
from shapely.ops import transform

from src.constants import (
    AGG_FEATURES,
    DATA_LINKS,
    DISTANCES,
    FEATURES,
    MODEL_PATH,
    PROBABILITY_THRESHOLD,
)


class DataOperator:
    data: gpd.GeoDataFrame
    explainer: shap.explainers.Tree

    def __init__(self) -> None:
        self.model = self.load_model()
        self.update_data()
        self.transform = self.get_transform()

    @staticmethod
    def load_model() -> Any:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        return model

    @staticmethod
    def get_transform() -> Callable[..., Tuple[Any, ...]]:
        wgs84 = pyproj.CRS("EPSG:4326")
        utm = pyproj.CRS("EPSG:3310")

        return pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform

    def load_data(self) -> None:
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
        gpd_data.rename(
            columns={"BRIGHT_TI4": "BRIGHTNESS", "BRIGHT_TI5": "BRIGHT_T31"},
            inplace=True,
        )
        gpd_data["CONFIDENCE_NAME"] = gpd_data["CONFIDENCE"]
        gpd_data["CONFIDENCE"] = gpd_data["CONFIDENCE"].map(
            {"l": 0, "h": 1, "n": 3, "high": 1, "nominal": 3, "low": 0}
        )
        gpd_data.crs = "epsg:4326"
        gpd_data.to_crs(epsg=3310, inplace=True)
        self.data = gpd_data
        self.data.reset_index(drop=True, inplace=True)

    def get_preds(self) -> None:
        gpd_data_initial = self.data.copy()
        for col in AGG_FEATURES:
            for agg in ["mean", "max", "min", "std"]:
                for dist in DISTANCES:
                    if agg == "std":
                        gpd_data_initial[f"{dist}.{col}.{agg}"] = 0
                    else:
                        gpd_data_initial[f"{dist}.{col}.{agg}"] = gpd_data_initial[col]
        for col in ["0.dist", "2.dist", "5.dist", "10.dist", "15.dist", "closest.dist"]:
            gpd_data_initial[col] = 0
        for col in AGG_FEATURES:
            gpd_data_initial[f"closest.{col}"] = gpd_data_initial[col]
        proba = self.model.predict_proba(gpd_data_initial[FEATURES])[:, 1]
        self.data["probability"] = proba
        self.data = self.data.loc[self.data["probability"] >= PROBABILITY_THRESHOLD, :]
        self.explainer = shap.TreeExplainer(self.model, gpd_data_initial[FEATURES])

    def update_data(self) -> None:
        self.load_data()
        self.get_preds()

    def get_agg(self, point: Point, distance: float) -> pd.DataFrame:
        indexes = self.data["geometry"].sindex.query(point.buffer(distance * 1000))
        subdata = self.data.iloc[indexes][AGG_FEATURES].agg(
            ["mean", "std", "max", "min"]
        )
        dist = 0
        for i in indexes:
            dist += self.data["geometry"].iloc[i].distance(point)
        subdata = pd.json_normalize({distance: subdata.to_dict()})
        count = max(1, len(indexes))
        subdata[f"{distance}.dist"] = dist / count
        return subdata

    def predict_point(self, lon: float, lat: float) -> Tuple[float, Any]:
        x = Point(lon, lat)
        x = transform(self.transform, x)
        series = []
        for dist in DISTANCES:
            series.append(self.get_agg(x, dist))
        series_df = pd.concat(series, axis=1)
        dists = self.data["geometry"].apply(lambda p: p.distance(x))
        index = dists.idxmin()
        series_df["closest.dist"] = dists.loc[index]
        for col in AGG_FEATURES:
            series_df[f"closest.{col}"] = self.data[col].loc[index]
        probability = self.model.predict_proba(series_df[FEATURES].fillna(0))[:, 1]
        shap_values = self.explainer.shap_values(series_df)
        return probability, shap_values
