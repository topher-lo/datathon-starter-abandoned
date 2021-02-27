# streamlit-e2e-boilerplate
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
[![Heroku Up](https://heroku-shields.herokuapp.com/traingenerator)](https://streamlit-e2e-boilerplate.herokuapp.com/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/)

🛠️📊 Boilerplate code for an end-to-end data app using pandas, Streamlit, and Prefect.

## ✨ Features
- Boilerplate code for data tasks across the data pipeline (preprocessing, modelling, post-processing)
- 5 common data tasks organised into individual functions (`retrieve_data`, `clean_data`, `transform_data`, `run_model`, and `plot_confidence_intervals`)
- An example data workflow (of the data tasks) orchestrated using Prefect.
- An example Streamlit application that demonstrates key commands in Streamlit's [API](https://docs.streamlit.io/en/stable/api.html#display-interactive-widgets) to:
    - Display text, data, status messages, and interactive widgets
    - Add a sidebar to the UI
    - Organise elements into side-by-side columns
- The example app also features:
    - 3 datasets from [R datasets](https://vincentarelbundock.github.io/Rdatasets/index.html) to plug in and play with
    - Automated EDA using pandas-profiling and missingno
    - A simple UI to run Prefect workflows
- Code follows Pandas best practices (e.g. method chaining) in a [modern idiomatic](https://tomaugspurger.github.io/modern-1-intro) style
- Custom [altair](https://altair-viz.github.io/) themes that match Streamlit's UI
- Fully documented functions, modules, and code (using inline comments)
- Containerised using docker and docker-compose
- Github Actions workflow for automated deployment to the Heroku Container Registry

## Install
streamlit-e2e-boilerplate has been tested with Python 3.8 and depends on the following packages:
- `pandas`
- `streamlit`
- `prefect`
- `altair`
- `statsmodels`
- `streamlit-pandas-profiling`
To use the boilerplate, you must first clone this repo:
```
git clone git@github.com:topher-lo/streamlit-e2e-boilerplate.git
cd [..path/to/repo]
```
Then install its dependencies using either pip:
```
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```
Or to run it as a containerised application using docker and docker-compose.
First create a file `.env` with the line:
```
PORT=8501
```
to specify which port to publish the data app to.
Then run the following commands on your CLI:
```
docker-compose build
docker-compose up -d
```

## 🏁 Getting started
To build your own app, M=modify pre-existing code and implement empty functions:
- Data tasks are found in `src/tasks.py`
- Data workflows are found in `src/pipeline.py`
- The Streamlit app's UI code is found in `app.py`
- Custom altair themes are found in `src/styles/altair.py`

## 🚀 A quick example
In your virtual environment, run the following command from the streamlit-e2e-boilerplate directory
```
streamlit run app.py
```
Then, the web app will be available at http://localhost:8501/
If you are using docker, the web app will be available at whichever port you specified in the `.env` file.

## 🗃️ Directory structure
TODO

## Deployment
- Heroku GH action

## Roadmap
- FastAPI
- Category (ordered/unordered)
- Missing values wrangler
- Additional models (generalised linear models, lagged variables)
- Prefect state handlers (e.g. send notification to slack)

## Contributing
