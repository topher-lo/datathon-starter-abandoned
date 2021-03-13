"""Runs the streamlit app.
Call this file in the terminal (from the `streamlit-e2e-boilerplate` dir)
via `streamlit run app.py`.
"""

import pandas as pd
import streamlit as st
import missingno as msno

from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

from src.pipeline import e2e_pipeline
from src.pipeline import wrangle_na_pipeline


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

    is_factor = st.sidebar.multiselect('Are there any categorical variables?',
                                       options=columns)
    cols_transf = st.sidebar.multiselect('Select columns to transform',
                                         options=columns)
    transf = st.sidebar.selectbox('Log or arcsinh transform?',
                                 options=['log', 'arcsinh'])
    endog = st.sidebar.selectbox('Select an endogenous variable'
                                 ' (must be numeric)',
                                 options=[None] + columns)
    exog = [col for col in columns if col != endog]
    na_strats = {
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
    na_strategy = na_strats[na_strategy_name]
    return {'url': url,
            'is_factor': is_factor,
            'cols_transf': cols_transf,
            'transf': transf,
            'endog': endog,
            'exog': exog,
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
        1. Data tasks are found in `src/tasks.py`
        2. Data workflows are found in `src/pipeline.py`
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
    kwargs = sidebar()  # Display sidebar in Streamlit app
    # Drop `data` and return its value
    data = kwargs.pop('data')
    # Drop dataset `item` code and return its value
    item = kwargs.pop('item')
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
            na_strategy = kwargs.get('na_strategy')
            state = wrangle_na_pipeline.run(data=data,
                                            na_strategy=na_strategy)
            task_ref = wrangle_na_pipeline.get_tasks(name='wrangle_na')[0]
            wrangled_data = state.result[task_ref].result
            st.write('')  # Insert blank line
            st.subheader('Wrangled Dataset')
            st.dataframe(wrangled_data)
    # Run data workflow
    if col4.button('✨ Run workflow!'):
        st.write('---')
        # Stop execution until a valid endogenous variable is selected
        if not(kwargs.get('endog')):
            st.warning('Please select an endogenous variable')
            st.stop()
        state = e2e_pipeline.run(**kwargs)
        state_msg = state.message  # Flow's outcome state's message
        # Check if all tasks were successfully executed
        if 'fail' in state_msg:
            # List of each state's (name, state message) in the workflow
            task_state_msgs = [(str(task), state.result[task].message) for task
                               in state.result.keys()]
            st.warning(state_msg)
            st.subheader('Workflow Logs')
            st.text('Note: the tasks below are not ordered by their run order.'
                    ' This will be fixed in a future version'
                    ' of the boilerplate.')
            task_state_table = (pd.DataFrame(task_state_msgs,
                                             columns=['task', 'state message'])
                                  .sort_values(by='task'))
            st.table(task_state_table)
        # If all tasks were successfully executed
        else:
            st.success(state_msg)
            st.subheader('Encoded Data')
            # Retrieve wrangled data from prefect pipeline
            task_name = 'encode_data'
            task_ref = e2e_pipeline.get_tasks(name=task_name)[0]
            encoded_data = state.result[task_ref].result
            st.dataframe(encoded_data)
            st.subheader('Regression Results')
            st.text('Dot and whisker plot of coefficients'
                    ' and their confidence intervals:')
            # Retrieve result value from prefect pipeline
            task_name = 'plot_confidence_intervals'
            task_ref = e2e_pipeline.get_tasks(name=task_name)[0]
            conf_int_chart = state.result[task_ref].result
            # Plot regression coefficient's confidence intervals
            st.altair_chart(conf_int_chart, use_container_width=True)


if __name__ == "__main__":
    main()
