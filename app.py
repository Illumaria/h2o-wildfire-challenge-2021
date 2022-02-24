import base64
import io
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import shap
from dash.dependencies import Input, Output, State
from shap.plots._force_matplotlib import draw_additive_plot

from src.constants import AGG_FEATURES, MAPBOX_TOKEN, FEATURES
from src.data_operator import DataOperator

app = dash.Dash(__name__)
data_operator = DataOperator()
LAST_UPDATE = datetime.now().date()


def update_data():
    now = datetime.now()
    if now.date() > LAST_UPDATE and now.hour > 3:
        data_operator.update_data()


@app.callback(Output("fire-map", "figure"), Input("proba_threshold", "value"))
def filter_by_proba(value):
    update_data()
    filtered_df = data_operator.data[
        data_operator.data["probability"] >= round(value / 100, 2)
    ]
    hover_data = {f: True for f in AGG_FEATURES}
    hover_data.update({"LATITUDE": False, "LONGITUDE": False, "probability": True})
    hover_data["CONFIDENCE"] = False
    hover_data["CONFIDENCE_NAME"] = True
    updated_fig = px.scatter_mapbox(
        filtered_df[
            AGG_FEATURES + ["LATITUDE", "LONGITUDE", "probability", "CONFIDENCE_NAME"]
        ],
        lat=filtered_df["LATITUDE"],
        lon=filtered_df["LONGITUDE"],
        color="probability",
        size="probability",
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=10,
        hover_data=hover_data,
        zoom=1,
    )
    return updated_fig


@app.callback(
    [Output("container-button-basic", "children")],
    [Input("submit-val", "n_clicks")],
    [State("input-lat", "value"), State("input-lon", "value")],
)
def update_output(n_clicks, lat, lon):
    if lat is None or lon is None:
        return ["Input lat and lon and press submit"]
    probability, shap_value = data_operator.predict_point(float(lon), float(lat))
    force_plot = shap.force_plot(
        data_operator.explainer.expected_value,
        shap_value[0],
        matplotlib=False,
        features=FEATURES
    )
    force_plot_mpl = draw_additive_plot(force_plot.data, (30, 7), show=False)
    tmpfile = io.BytesIO()
    force_plot_mpl.savefig(tmpfile, format="png")
    encoded = base64.b64encode(tmpfile.getvalue()).decode("utf-8")
    shap_html = html.Img(src=f"data:image/png;base64, {encoded}")
    return [shap_html]


if __name__ == "__main__":
    px.set_mapbox_access_token(MAPBOX_TOKEN)
    app.layout = html.Div(
        [
            html.H1(children="World fires"),
            html.Div(children="This data was provided by the NASA FIRES"),
            html.Div(
                [
                    dcc.Graph(
                        id="fire-map",
                        style={
                            "width": "95%",
                            "height": "100%",
                            "display": "inline-block",
                            "position": "relative",
                        },
                    ),
                    html.Div(
                        [
                            dcc.Slider(
                                id="proba_threshold",
                                max=100,
                                min=5,
                                step=5,
                                value=5,
                                updatemode="drag",
                                marks={
                                    i: "{}".format(round(i / 100, 2))
                                    for i in range(5, 105, 5)
                                },
                                vertical=True,
                            )
                        ],
                        style={
                            "height": "100%",
                            "width": "3%",
                            "display": "inline-block",
                            "position": "relative",
                        },
                    ),
                ],
                style={"height": "70vh"},
            ),
            html.Div(
                [
                    html.Div([
                        html.Label(
                            "latitude",
                            style={"marginRight": "10px", "width": "5%"},
                        ),
                        dcc.Input(
                            id="input-lat",
                            type="text",
                            placeholder="input latitude",
                        ),

                    ]),
                    html.Div([
                        html.Label(
                            "longitude",
                            style={"marginRight": "10px", "width": "5%"},
                        ),
                        dcc.Input(
                            id="input-lon",
                            type="text",
                            placeholder="input longitude"
                        )
                    ]),
                    html.Button("Submit", id="submit-val", n_clicks=0),
                    html.Div(id="container-button-basic", style={"width: 100%"})
                ]
            ),
        ]
    )
    app.run_server(host="0.0.0.0", port=4400)
