import asyncio
import json
import threading
from datetime import datetime

import plotly
import plotly.express as px
from flask import Flask, make_response, render_template

from src.constants import MAPBOX_TOKEN
from src.utils import init_models, predict_fires, update_data

app = Flask(__name__)
app.config['current_data'] = None
app.config['current_fires'] = None
app.config['model_cbc'] = None
app.config['model_lgb'] = None


async def schedule() -> None:
    while True:
        current_dt = datetime.now()
        if current_dt.hour == 3 and current_dt.minute > 30:
            app.config['current_data'] = update_data()
            app.config['current_fires'] = predict_fires(
                app.config['model_cbc'],
                app.config['model_lgb'],
                app.config['current_data'],
            )
        await asyncio.sleep(1800)


def wrapper(run_loop) -> None:
    asyncio.set_event_loop(run_loop)
    loop.run_until_complete(schedule())


@app.route('/map')
def draw_map():
    px.set_mapbox_access_token(MAPBOX_TOKEN)

    fig = px.scatter_mapbox(
        app.config['current_fires'],
        lat=app.config['current_fires']['LATITUDE'],
        lon=app.config['current_fires']['LONGITUDE'],
        color='predict_proba',
        size='predict_proba',
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=10,
        zoom=1,
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('map.html', graphJSON=graphJSON)


@app.route('/')
def health():
    return make_response('Ok', 200)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    thread = threading.Thread(target=wrapper, args=(loop,))
    thread.start()
    app.config['model_cbc'], app.config['model_lgb'] = init_models()
    app.config['current_data'] = update_data()
    app.config['current_fires'] = predict_fires(
        app.config['model_cbc'],
        app.config['model_lgb'],
        app.config['current_data'],
    )
    app.run(host='0.0.0.0', port=4400)
