"""This module registers flows to be managed by the Prefect Backend.
"""

from src.pipeline import e2e_pipeline
from src.pipeline import wrangle_na_pipeline


# Register Flows
PROJECT_NAME = 'streamlit-e2e-boilerplate'
wrangle_na_pipeline.register(project_name=PROJECT_NAME)
e2e_pipeline.register(project_name=PROJECT_NAME)