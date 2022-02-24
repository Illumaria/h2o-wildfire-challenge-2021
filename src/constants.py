NASA_LINK = 'https://firms.modaps.eosdis.nasa.gov/data/active_fire'
DATA_LINKS = [
    f'{NASA_LINK}/suomi-npp-viirs-c2/shapes/zips/SUOMI_VIIRS_C2_Global_24h.zip',
    f'{NASA_LINK}/noaa-20-viirs-c2/shapes/zips/J1_VIIRS_C2_Global_24h.zip',
]

CATBOOST_PATH = 'models/catboost.cbm'
MODEL_PATH = 'models/model.pkl'

AGG_FEATURES = ["BRIGHTNESS", "BRIGHT_T31", "FRP", "CONFIDENCE"]
DISTANCES = [0, 2, 5, 10, 15]
FEATURES = [
    '0.BRIGHTNESS.mean', '0.BRIGHTNESS.std', '0.BRIGHTNESS.max',
    '0.BRIGHTNESS.min', '0.BRIGHT_T31.mean', '0.BRIGHT_T31.std',
    '0.BRIGHT_T31.max', '0.BRIGHT_T31.min', '0.FRP.mean', '0.FRP.std',
    '0.FRP.max', '0.FRP.min', '0.CONFIDENCE.mean', '0.CONFIDENCE.std',
    '0.CONFIDENCE.max', '0.CONFIDENCE.min', '2.BRIGHTNESS.mean',
    '2.BRIGHTNESS.std', '2.BRIGHTNESS.max', '2.BRIGHTNESS.min',
    '2.BRIGHT_T31.mean', '2.BRIGHT_T31.std', '2.BRIGHT_T31.max',
    '2.BRIGHT_T31.min', '2.FRP.mean', '2.FRP.std', '2.FRP.max',
    '2.FRP.min', '2.CONFIDENCE.mean', '2.CONFIDENCE.std',
    '2.CONFIDENCE.max', '2.CONFIDENCE.min', '5.BRIGHTNESS.mean',
    '5.BRIGHTNESS.std', '5.BRIGHTNESS.max', '5.BRIGHTNESS.min',
    '5.BRIGHT_T31.mean', '5.BRIGHT_T31.std', '5.BRIGHT_T31.max',
    '5.BRIGHT_T31.min', '5.FRP.mean', '5.FRP.std', '5.FRP.max',
    '5.FRP.min', '5.CONFIDENCE.mean', '5.CONFIDENCE.std',
    '5.CONFIDENCE.max', '5.CONFIDENCE.min', '10.BRIGHTNESS.mean',
    '10.BRIGHTNESS.std', '10.BRIGHTNESS.max', '10.BRIGHTNESS.min',
    '10.BRIGHT_T31.mean', '10.BRIGHT_T31.std', '10.BRIGHT_T31.max',
    '10.BRIGHT_T31.min', '10.FRP.mean', '10.FRP.std', '10.FRP.max',
    '10.FRP.min', '10.CONFIDENCE.mean', '10.CONFIDENCE.std',
    '10.CONFIDENCE.max', '10.CONFIDENCE.min', '15.BRIGHTNESS.mean',
    '15.BRIGHTNESS.std', '15.BRIGHTNESS.max', '15.BRIGHTNESS.min',
    '15.BRIGHT_T31.mean', '15.BRIGHT_T31.std', '15.BRIGHT_T31.max',
    '15.BRIGHT_T31.min', '15.FRP.mean', '15.FRP.std', '15.FRP.max',
    '15.FRP.min', '15.CONFIDENCE.mean', '15.CONFIDENCE.std',
    '15.CONFIDENCE.max', '15.CONFIDENCE.min', "0.dist", "2.dist",
    "5.dist", "10.dist", "15.dist", "closest.dist", "closest.BRIGHTNESS",
    "closest.BRIGHT_T31", "closest.FRP", "closest.CONFIDENCE"
]
MAPBOX_TOKEN = 'pk.eyJ1IjoiaW1keGRkIiwiYSI6ImNreDdkcml0YjAxMDAyd3Q4aXhyb3ByanYifQ.9qBe9y5Q9vL9J9SA0x6f6g'
PROBABILITY_THRESHOLD = 0.2
