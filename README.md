# streamlit-e2e-boilerplate
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/)

🛠️📊 Boilerplate code for an end-to-end data app using pandas, Streamlit, and Prefect.

### Motivation
I made this project with two aims. First, as starter code for my own data projects. Second, as a "learning-by-doing" project to gather and apply best-practices in pandas, data workflows, and statistics. As my work is primarily in causal machine learning, the boilerplate is slightly biased towards econometrics and user-driven data workflows. Nevertheless, by releasing this code, I hope it can be useful to others when they begin to build their own data app.

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
- `altair`
- `pandas`
- `prefect`
- `statsmodels`
- `sklearn`
- `streamlit`
- `streamlit-pandas-profiling`
- `missingno`
This boilerplate also depends on Prefect Server, which requires `docker` and `docker-compose` to be installed and running.

To use the boilerplate, there are three steps. First, you clone this repo:
```bash
git clone git@github.com:topher-lo/streamlit-e2e-boilerplate.git
cd [..path/to/repo]
```
Second, install its dependencies using either pip:
```bash
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```
Or run it as a containerised application using docker and docker-compose.
First create a file `.env` with the line:
```
PORT=8501
```
to specify which port to publish the data app to.
Then run the following commands on your CLI:
```bash
docker-compose build
docker-compose up -d
```
Lastly, configure Prefect for local orchestration:
```bash
prefect backend server
```
Then start the Prefect server:
```bash
prefect server start
```
And register all flows with the server by running:
```bash
python register_flows.py
```
Note that Prefect comes with a web-based UI for orchestrating and managing flows.
Once the server's running, the UI can be viewed by visiting [localhost:8080](http://localhost:8080).
Moreover, Prefect exposes a GraphQL API for interacting with the platform.
The API can be accessed through [localhost:4200](http://localhost:4200).


## 🏁 Getting started
To build your own app, modify pre-existing code and implement empty functions:
- Data tasks are found in `server/tasks.py`
- Data workflows are found in `server/pipeline.py`
- The Streamlit app's UI code is found in `app.py`
- Custom altair themes are found in `server/styles/altair.py`

## 🚀 A quick example
In your virtual environment, run the following command from the `streamlit-e2e-boilerplate` dir:
```bash
streamlit run app.py
```
The web app will be available at http://localhost:8501/
Otherwise, if you are using docker, the web app will be available at whichever port you specified in the `.env` file.

## 🗃️ Directory structure
```
├── streamlit-e2e-boilerplate
    ├── client
    │   ├── app.py
    │   ├── __init__.py
    │   ├── results
    │   └── tests
    │       ├── __init__.py
    │       └── test_app.py
    ├── conftest.py
    ├── CONTRIBUTING.md
    ├── docker-compose.yml
    ├── Dockerfile
    ├── .gitignore
    ├── LICENSE
    ├── pipeline.ini
    ├── pytest.ini
    ├── README.md
    ├── register_flows.py
    ├── requirements-dev.txt
    ├── requirements.txt
    └── server
        ├── client
        │   └── results
        ├── __init__.py
        ├── pipeline.py
        ├── styles
        │   ├── altair.py
        │   └── __init__.py
        ├── tasks.py
        ├── tests
        │   ├── __init__.py
        │   └── test_tasks.py
        └── utils.py
```

## Contributing
Found a bug? Wrote a patch? Want to add a new feature, suggest changes to the API, or improve the docs? Please checkout the brief [contribution guide](https://github.com/topher-lo/streamlit-e2e-boilerplate/blob/main/CONTRIBUTING.md). Any and all contributions are welcome. ❤️📊🙌

## Getting in touch
If you are having a problem with streamlit-e2e-boilerplate, please raise a GitHub issue. For anything else, you can reach me at: lochristopherhy@gmail.com
