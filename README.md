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
- pip env
- docker (build and up)

## 🏁 Getting started
- Data tasks
- Data pipeline
- UI

## 🚀 A quick example
- streamlit run app.py

## 🗃️ Directory structure

## Deployment
- Heroku GH action

## Roadmap
- FastAPI
- Category (ordered/unordered)
- Missing values wrangler
- Additional models (generalised linear models, lagged variables)
- Prefect state handlers (e.g. send notification to slack)

## Contributing
