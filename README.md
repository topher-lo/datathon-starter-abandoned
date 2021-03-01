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
- `altair`
- `pandas`
- `prefect`
- `statsmodels`
- `streamlit`
- `streamlit-pandas-profiling`
- `missingno`

To use the boilerplate, you must first clone this repo:
```bash
git clone git@github.com:topher-lo/streamlit-e2e-boilerplate.git
cd [..path/to/repo]
```
Then install its dependencies using either pip:
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

## 🏁 Getting started
To build your own app, modify pre-existing code and implement empty functions:
- Data tasks are found in `src/tasks.py`
- Data workflows are found in `src/pipeline.py`
- The Streamlit app's UI code is found in `app.py`
- Custom altair themes are found in `src/styles/altair.py`

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
    ├── app.py
    ├── CONTRIBUTING.md
    ├── docker-compose.yml
    ├── Dockerfile
    ├── LICENSE
    ├── README.md
    ├── requirements.txt
    └── src
        ├── __init__.py
        ├── pipeline.py
        ├── styles
        │   ├── altair.py
        │   ├── __init__.py
        ├── tasks.py
        └── utils.py
```

## Deployment
To deploy to Heroku via Github actions, first generate a Heroku [API key](https://help.heroku.com/PBGP6IDE/how-should-i-generate-an-api-key-that-allows-me-to-use-the-heroku-platform-api). Save this key as `HEROKU_API_KEY` in your Github repo's [secrets](https://docs.github.com/en/actions/reference/encrypted-secrets). Second, create a Heroku app either via the [CLI](https://devcenter.heroku.com/articles/creating-apps) or the web-based [dashboard](https://devcenter.heroku.com/articles/heroku-dashboard). Save the name of your app as `HEROKU_APP_NAME` in your Github repo's secrets.

Create a new branch from the main branch called `prod`:
```bash
git checkout main
git branch prod
git push origin prod
```
This branch is used for production. Any code that is pushed to this branch will be automatically deployed to Heroku. Note: I am looking to include multiple deployment strategies (e.g. AWS Elastic Beanstalk, Azure Container Registry) in future versions of the boilerplate.

## Roadmap
I will implement the following features depending on this repo's popularity (i.e. number of stars):
- [5 stars] Introduce pandas's API for dealing with ordered and unordered categories
- [10 stars] Implement a missing values wrangler (e.g. multiple imputation)
- [25 stars] Implement additional baseline models (generalised linear models, random forest)
- [50 stars] Separate out the backend (data tasks and workflow) into [FastAPI](https://github.com/tiangolo/fastapi) for other applications to call
- [80 stars] Implement automated deployment to AWS Elastic Beanstalk and Azure Container Registry via Github Actions

## Contributing
Found a bug? Wrote a patch? Want to add a new feature, suggest changes to the API, or improve the docs? Please checkout the brief [contribution guide](https://github.com/topher-lo/streamlit-e2e-boilerplate/blob/main/CONTRIBUTING.md). Any and all contributions are welcome. ❤️📊🙌

## Getting in touch
If you are having a problem with streamlit-e2e-boilerplate, please raise a GitHub issue. For anything else, you can reach me at: lochristopherhy@gmail.com


