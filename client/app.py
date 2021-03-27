"""Runs the streamlit app.
Call this file in the terminal (from the `streamlit-e2e-boilerplate` dir)
via `streamlit run app.py`.
"""

import pandas as pd
import prefect
import streamlit as st
import missingno as msno
import time

from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from typing import List
from typing import Mapping

from prefect.client.client import Client

from prefect.tasks.prefect.flow_run import StartFlowRun
from prefect.engine.results.local_result import LocalResult


R_DATASETS_URL = 'https://vincentarelbundock.github.io/Rdatasets'
DATASET_URLS = {
    'SmokeBan': f'{R_DATASETS_URL}/csv/AER/SmokeBan.csv',
    'airquality': f'{R_DATASETS_URL}/csv/datasets/airquality.csv',
    'TeachingRatings': f'{R_DATASETS_URL}/csv/AER/TeachingRatings.csv',
}  # A few example datasets to get you started
DATASET_DOCS_URLS = {
    'SmokeBan': f'{R_DATASETS_URL}/doc/AER/SmokeBan.html',
    'airquality': f'{R_DATASETS_URL}/doc/datasets/airquality.html',
    'TeachingRatings': f'{R_DATASETS_URL}/doc/AER/TeachingRatings.html',
}
DATASET_TITLES = {
    'SmokeBan': 'Do Workplace Smoking Bans Reduce Smoking?',
    'airquality': 'New York Air Quality Measurements',
    'TeachingRatings': 'Impact of Beauty on Instructor\'s Teaching Ratings',
}


def create_prefect_flow_run(flow_name: str,
                            project_name: str,
                            task_refs: List,
                            params: Mapping) -> str:
    """Creates new prefect flow run for given flow id, parameters, task references
    and API server URL to send GraphQL requests to.
    Returns results value and state from a Prefect flow run.
    """

    try:
        flow_run = StartFlowRun(flow_name=flow_name,
                                project_name=project_name,
                                parameters=params)
        flow_run_id = flow_run.run()
        client = Client()
        while True:
            time.sleep(10)
            flow_run_info = client.get_flow_run_info(flow_run_id)
            flow_state = flow_run_info.state
            task_runs_info = flow_run_info.task_runs
            if flow_state.is_finished():
                task_res_locs = {}
                for task_run in task_runs_info:
                    # Return ref if ref string is a substring of any task slug
                    ref = next((ref_str for ref_str in task_refs
                                if ref_str in task_run.task_slug), None)
                    if ref:
                        task_id = task_run.id
                        state = client.get_task_run_state(task_id)
                        task_res_locs[ref] = state._result.location
                task_results = {}
                for ref, loc in task_res_locs.items():
                    local_res = LocalResult()
                    result = local_res.read(loc)
                    task_results[ref] = result.value
                return task_results, flow_state
    except ValueError as err:
        raise err


def sidebar():
    """Write Streamlit commands here to display text and widgets in the sidebar.
    Replace the code within this function with your own
    interactive components and UI.
    """

    st.sidebar.markdown(
        """
        ## Datasets
        Three datasets from [R datasets]({}) are provided:
        - Do Workplace Smoking Bans Reduce Smoking
        - New York Air Quality Measurements
        - Impact of Beauty on Instructor's Teaching Ratings
        """.format(R_DATASETS_URL)
    )
    datasets = [None] + list(DATASET_URLS.keys())
    dataset_item = st.sidebar.selectbox('Which dataset are you interested in?',
                                        options=datasets)

    # Stop execution until a valid dataset is selected
    if not dataset_item:
        st.stop()
    url = DATASET_URLS[dataset_item]
    doc = DATASET_DOCS_URLS[dataset_item]
    # Read first row of csv file
    raw = pd.read_csv(url)
    data = raw.loc[:, ~raw.columns.str.contains('Unnamed')]
    columns = data.columns.tolist()

    st.sidebar.subheader('Model Specification')
    st.success(f'Successfully loaded dataset: {dataset_item}')
    st.info(f'URL found [here]({url}). Documentation found [here]({doc}).')

    cat_cols = st.sidebar.multiselect('Are there any categorical variables?',
                                      options=columns)
    transformed_cols = st.sidebar.multiselect('Select columns to transform',
                                              options=columns)
    transf = st.sidebar.selectbox('Log or arcsinh transform?',
                                  options=['log', 'arcsinh'])
    endog = st.sidebar.selectbox('Select an endogenous variable'
                                 ' (must be numeric)',
                                 options=[None] + columns)
    exog = [col for col in columns if col != endog]
    na_strategies = {
        'Complete case': 'cc',
        'Fill-in': 'fi',
        'Fill-in with indicators': 'fii',
        'Grand model': 'gm',
        'MICE': 'mice',
    }
    na_strategy_name = st.sidebar.selectbox(
        'How should missing values be dealt with?',
        options=[
          'Complete case',
          'Fill-in',
          'Fill-in with indicators',
          'Grand model',
          'MICE'
        ])
    na_values_string = st.sidebar.text_input(
        'Are there any text values that should be recognised as NA?'
        ' (separate values with a comma)',
        'Missing, missing, not found'
    )
    na_values = [s.strip() for s in na_values_string.split(',')]
    na_strategy = na_strategies[na_strategy_name]
    return {'url': url,
            'cat_cols': cat_cols,
            'transformed_cols': transformed_cols,
            'transf': transf,
            'endog': endog,
            'exog': exog,
            'na_values': na_values,
            'na_strategy': na_strategy,
            'data': data,
            'item': dataset_item}


def main():
    """Write Streamlit commands here to display text and data in the app.
    Replace the code within this function with your own data workflow and UI.

    Streamlit API reference:
    https://docs.streamlit.io/en/stable/api.html
    """

    # Configures the default settings
    st.set_page_config(page_title='streamlit-e2e-boilerplate',
                       page_icon='🛠️',
                       layout='wide')

    # Page title and header
    st.title('🛠️📊')
    st.title('Boilerplate for data applications')
    st.subheader('MIT License')
    st.markdown(
        """
        ---
        🙌 Build your own data app

        Modify pre-existing code and implement empty functions:\n
        1. Data tasks are found in `server/tasks.py`
        2. Data workflows are found in `server/pipeline.py`
        3. The Streamlit app's UI code is found in `app.py`
        ---
        🚀 Try a quick example

        From the sidebar *(click on > if closed)*:\n
        1. Select a dataset
        2. Select all categorical variables in the multiselect widget
        3. Select an endogenous variable in the chosen dataset

        From the main UI below:\n
        4. Press the "Run workflow" button
        ---
        """
    )

    # Example app
    params = sidebar()  # Display sidebar in Streamlit app
    # Drop `data` and return its value
    data = params.pop('data')
    # Drop dataset `item` code and return its value
    item = params.pop('item')
    title = DATASET_TITLES[item]
    st.subheader(f'{title}')
    st.text('A random sample of 5 rows:')
    st.table(data.sample(5))  # Display random sample as a static table

    # Column container for buttons
    col1, col2, col3, col4 = st.beta_columns(4)
    # Data profiling
    if col1.button('🔬 Data profiling report'):
        profile_report = ProfileReport(data, explorative=True)
        st_profile_report(profile_report)
    # Missing value analysis
    if col2.button('🔎 Missing value plots'):
        # Check if there are any missing values
        if pd.notna(data).all().all():
            st.warning('No missing values in dataset')
        else:
            fig1 = msno.matrix(data).get_figure()
            st.pyplot(fig1)
            fig2 = msno.heatmap(data).get_figure()
            st.pyplot(fig2)
            fig3 = msno.dendrogram(data).get_figure()
            st.pyplot(fig3)
    # Missing value wrangler
    if col3.button('🕵️ Wrangle NA values'):
        # Check if there are any missing values
        if pd.notna(data).all().all():
            st.warning('No missing values in dataset')
        else:
            na_strategy = params.get('na_strategy')
            flow_name = 'wrangle_na_pipeline'
            project_name = 'streamlit-e2e-boilerplate'
            task_refs = ['wrangle_na']
            params = {'url': params.get('url'),
                      'sep': params.get('sep'),
                      'strategy': na_strategy}
            results, _ = create_prefect_flow_run(flow_name,
                                                 project_name,
                                                 task_refs,
                                                 params)
            st.write('')  # Insert blank line
            st.subheader('Wrangled Dataset')
            st.dataframe(results['wrangle_na'])
    # Run data workflow
    if col4.button('✨ Run workflow!'):
        st.write('---')
        # Stop execution until a valid endogenous variable is selected
        if not(params.get('endog')):
            st.warning('Please select an endogenous variable')
            st.stop()
        flow_name = 'e2e_pipeline'
        project_name = 'streamlit-e2e-boilerplate'
        task_refs = ['wrangle_na']
        params = {'url': params.get('url'),
                  'sep': params.get('sep'),
                  'strategy': na_strategy}
        results, state_msg = create_prefect_flow_run(flow_name,
                                                     project_name,
                                                     task_refs,
                                                     params)
        # Check if all tasks were successfully executed
        if 'fail' in state_msg:
            # List of each state's (name, state message) in the workflow
            st.warning(state_msg)
            st.info('Please view the Flow logs on the Prefect Server\'s'
                    ' [UI](localhost:8080).')
        # If all tasks were successfully executed
        else:
            # Unpack results
            preprocessed_data, conf_int_chart = results
            # Success!
            st.balloons()
            st.success(state_msg)
            # Retrieve results from prefect flow run
            st.subheader('Pre-processed Data')
            st.dataframe(preprocessed_data)
            st.subheader('Regression Results')
            st.text('Dot and whisker plot of coefficients'
                    ' and their confidence intervals:')
            # Plot regression coefficient's confidence intervals
            st.altair_chart(conf_int_chart, use_container_width=True)


if __name__ == "__main__":
    main()
