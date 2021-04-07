# streamlit-e2e-boilerplate
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
[![codecov](https://codecov.io/gh/topher-lo/streamlit-e2e-boilerplate/branch/main/graph/badge.svg?token=6J0IJ3EVPQ)](https://codecov.io/gh/topher-lo/streamlit-e2e-boilerplate)
[![Run Server Tests](https://github.com/topher-lo/streamlit-e2e-boilerplate/workflows/Run%20Server%20Tests/badge.svg)](https://github.com/topher-lo/streamlit-e2e-boilerplate/actions)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/)


🛠️📊 Boilerplate code for an end-to-end data app using pandas, Streamlit, and Prefect.

### Project Status:
- Dockerised app not working under new client/server architecture (TO FIX)

### Motivation
I made this project with two aims. First, as starter code for my own data projects. Second, as a "learning-by-doing" project to gather and apply best-practices in pandas, data workflows, and statistics. As my work is primarily in causal machine learning, the boilerplate is slightly biased towards econometrics and user-driven data workflows. Nevertheless, by releasing this code, I hope it can be useful to others when they begin to build their own data app.

## ✨ Features
- Boilerplate code for data tasks across the data pipeline (preprocessing, modelling, post-processing)
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
Lastly, set-up Prefect Server and deploy flows.
1. Configure Prefect for local orchestration:
```bash
prefect backend server
```
2. Start the Prefect Server:
```bash
prefect server start
```
3. Register all flows with the server by running:
```bash
python register_flows.py
```
4. Start a Prefect Agent to execute and monitor Flow runs:
```bash
prefect agent start
```
Note: Prefect comes with a web-based UI for orchestrating and managing flows.
Once the server's running, this UI can be viewed by visiting [localhost:8080](http://localhost:8080).
Moreover, Prefect exposes a GraphQL API for interacting with the platform.
This API can be accessed through [localhost:4200](http://localhost:4200).


## 🏁 Getting started
To build your own app, modify pre-existing code and implement empty functions:
- Data tasks are found in `server/tasks.py`
- Data workflows are found in `server/pipeline.py`
- The Streamlit app's UI code is found in `client/app.py`
- Custom altair themes are found in `server/styles/altair.py`

## 🚀 A quick example
In your virtual environment, run the following command from the `streamlit-e2e-boilerplate/client` dir:
```bash
streamlit run app.py
```
The web app will be available at http://localhost:8501/

## Contributing
Found a bug? Wrote a patch? Want to add a new feature, suggest changes to the API, or improve the docs? Please checkout the brief [contribution guide](https://github.com/topher-lo/streamlit-e2e-boilerplate/blob/main/CONTRIBUTING.md). Any and all contributions are welcome. ❤️📊🙌

## Getting in touch
If you are having a problem with streamlit-e2e-boilerplate, please raise a GitHub issue. For anything else, you can reach me at: lochristopherhy@gmail.com
