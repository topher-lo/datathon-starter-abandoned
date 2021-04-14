# streamlit-e2e-boilerplate
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
[![codecov](https://codecov.io/gh/topher-lo/streamlit-e2e-boilerplate/branch/main/graph/badge.svg?token=6J0IJ3EVPQ)](https://codecov.io/gh/topher-lo/streamlit-e2e-boilerplate)
[![Run tests](https://github.com/topher-lo/streamlit-e2e-boilerplate/workflows/Run%20tests/badge.svg)](https://github.com/topher-lo/streamlit-e2e-boilerplate/actions)
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
streamlit-e2e-boilerplate has been tested with Python 3.8. Dependencies for the Streamlit app and Prefect server can be found in `client/requirements.txt` and `server/requirements.txt` respectively.

This boilerplate also requires Docker and a Kubernetes cluster to be installed and running.


## 🏁 Getting started
To build your own app, modify pre-existing code and implement empty functions:
- Data tasks are found in `server/src/tasks.py`
- Data workflows are found in `server/src/pipeline.py`
- The Streamlit app's UI code is found in `client/app.py`
- Custom altair themes are found in `server/src/styles/altair.py`

## 🚀 Deployment to Digital Ocean
TODO

## Contributing
Found a bug? Wrote a patch? Want to add a new feature, suggest changes to the API, or improve the docs? Please checkout the brief [contribution guide](https://github.com/topher-lo/streamlit-e2e-boilerplate/blob/main/CONTRIBUTING.md). Any and all contributions are welcome. ❤️📊🙌

## Getting in touch
If you are having a problem with streamlit-e2e-boilerplate, please raise a GitHub issue. For anything else, you can reach me at: lochristopherhy@gmail.com
