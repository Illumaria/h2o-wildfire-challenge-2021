# H2O Wildfire Challenge

## Purpose

The application is designed to show the points of possible fire occurences on the world map.

The solution is expected to mostly help the local authorities to prepare for possible threats, but can easily be used by anyone concerned about random fires in their area.

## Training

The training process can be reconstructed in two steps:
1. First, collect the training data. We used [FIRMS](https://firms.modaps.eosdis.nasa.gov/download/) (NASA temperature anomaly data). See `notebooks/collect_data.ipynb` for details.
2. Train models on that data. See `notebooks/train.ipynb` for details.
3. Place both models in `models` folder to use them in the application. We provide pretrained models so that the application is ready to use.

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

## Team members

This solution was developed by [Anton Nesterenko](https://github.com/IMDxD), [Yuri Bolkonsky](https://github.com/YuryBolkonsky), and [Dmitry Astankov](https://github.com/illumaria).