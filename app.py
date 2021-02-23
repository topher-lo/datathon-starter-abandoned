"""Runs the streamlit app.
Call this file in the terminal (from the `streamlit-e2e-boilerplate` dir)
via `streamlit run app.py`.
"""

import streamlit as st


def main():
    """Write Streamlit commands here to display text and data in the app.
    """
    # Configures the default settings
    st.set_page_config(page_title='streamlit-e2e-boilerplate',
                       page_icon='🧰')
    st.title('Hello world.')


if __name__ == "__main__":
    main()
