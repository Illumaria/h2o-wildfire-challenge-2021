NASA_LINK = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire'
DATA_LINKS = [
    f'{NASA_LINK}/suomi-npp-viirs-c2/shapes/zips/SUOMI_VIIRS_C2_Global_24h.zip',
    # f'{NASA_LINK}/modis-c6.1/shapes/zips/MODIS_C6_1_Global_24h.zip',
    f'{NASA_LINK}/noaa-20-viirs-c2/shapes/zips/J1_VIIRS_C2_Global_24h.zip',
]

CATBOOST_PATH = 'models/catboost.cbm'
LIGHTGBM_PATH = 'models/light_gbm.txt'

FEATURES = [
    'LATITUDE',
    'LONGITUDE',
    'BRIGHTNESS',
    'SCAN',
    'TRACK',
    'ACQ_TIME',
    'SATELLITE',
    'DAYNIGHT',
    'CONFIDENCE',
    'BRIGHT_T31',
    'FRP',
]

MAPBOX_TOKEN = 'pk.eyJ1IjoiaW1keGRkIiwiYSI6ImNreDdkcml0YjAxMDAyd3Q4aXhyb3ByanYifQ.9qBe9y5Q9vL9J9SA0x6f6g'
PROBABILITY_THRESHOLD = 0.25
