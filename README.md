# H2O Wildfire Challenge

## Purpose

The application is designed to show the points of possible fire occurrences on the world map. The model is trained on historical data, but at inference time it takes real daily data and makes predictions for it.

The solution is expected to mostly help the local authorities to prepare for possible threats, but can easily be used by anyone concerned about random fires in their area.

## Approaches

For this solution, we decided to stick with Gradient Boosting methods (specifically CatBoost) due to their undoubted advantages: they work well for tabular data, fairly fast to train, and allow for good interpretability.  

## Training

The training process can be reconstructed in two steps:
1. First, collect the training data. We used [FIRMS](https://firms.modaps.eosdis.nasa.gov/download/) (NASA temperature anomaly data). See `notebooks/collect_data.ipynb` for details.
2. Train models on that data. See [`notebooks/baseline_new.ipynb`](https://github.com/Illumaria/h2o-wildfire-challenge-2021/blob/master/notebooks/baseline_new.ipynb) for details.

Place the resulting model in `models` folder to use it in the application. We provide pretrained model so that the application is ready to use.

## Usage

With conda environment:

```bash
conda env create -f environment.yml
conda activate h2o-wildfire
python app.py
```

With local environment and pip:

```bash
pip install -r requirements.txt
python app.py
```

With Docker:

```bash
docker build -t h2o-wildfire .
docker run --rm -p 4400:4400 h2o-wildfire
```

Now go to the `https://localhost:4400/map`! :)
It is possible to set threshold for model confidence (see the vertical slider on the right side of the page) to filter points, or to get predictions _and_ their explanations (we used Shapley values) for the exact location by providing its latitude and longitude. 

## Team members

This solution was developed by [Anton Nesterenko](https://github.com/IMDxD), [Yuri Bolkonsky](https://github.com/YuryBolkonsky), and [Dmitry Astankov](https://github.com/illumaria).
