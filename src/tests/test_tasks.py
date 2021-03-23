import numpy as np
import pandas as pd
import pytest

from io import StringIO

from pandas.testing import assert_frame_equal
from pandas.testing import assert_index_equal
from numpy.testing import assert_allclose
from numpy.testing import assert_equal

from src.tasks import _column_wrangler
from src.tasks import _obj_wrangler


# TESTCASES

STR_NA_VALUES = [
    "-1.#IND",
    "1.#QNAN",
    "1.#IND",
    "-1.#QNAN",
    "#N/A N/A",
    "#N/A",
    "N/A",
    "n/a",
    "NA",
    "<NA>",
    "#NA",
    "NULL",
    "null",
    "NaN",
    "-NaN",
    "nan",
    "-nan",
    "",
]  # Strings recognised as NA/NaN by Pandas

STR_DATA_EXAMPLES = {
    # Time series data with integer and binary cols (no range index)
    'us_consump_1940s':
        """
        "year","income","expenditure","war",
        "1940",241,226,0
        "1941",280,240,0
        "1942",319,235,1
        "1943",331,245,1
        "1944",345,255,1
        "1945",340,265,1
        "1946",332,295,0
        "1947",320,300,0
        "1948",339,305,0
        "1949",338,315,0
        """,
    # Cross-sectional data with float, string, factor, binary, and boolean cols
    'iraq_vote':
        """
        ,"y","state.abb","name","rep","state.name","gorevote"
        1,1,"AL","SESSIONS (R AL)",TRUE,"Alabama",41.59
        2,0,"CA","BOXER (D CA)",FALSE,"California",53.45
        3,0,"HI","INOUYE (D HI)",FALSE,"Hawaii",55.79
        4,1,"ID","CRAIG (R ID)",TRUE,"Idaho",27.64
        5,1,"ID","CRAPO (R ID)",TRUE,"Idaho",27.64
        6,0,"IL","DURBIN (D IL)",FALSE,"Illinois",54.6
        7,1,"IL","FITZGERALD (R IL)",TRUE,"Illinois",54.6
        8,0,"VT","LEAHY (D VT)",FALSE,"Vermont",50.63
        9,1,"VA","WARNER (R VA)",TRUE,"Virginia",44.44
        10,1,"WA","CANTWELL (D WA)",FALSE,"Washington",50.13
        """,
    # Air quality TSV data (with missing values)
    # Row 4: 1 NA, Row 5: 2 NA, Row 10: 3 NA
    # Mean = 23.85714, 172.62500, 12.35556. 0.66667
    # Mode (Dummy col) = 1
    'airquality_na':
        """
        ,Ozone,Solar.R,Wind,Dummy
        1,41,190,7.4,0
        2,36,118,8,0
        3,12,149,12.6,0
        4,NA,313,11.5,1
        5,NA,,14.3,1
        6,28,,14.9,1
        7,23,299,8.6,1
        8,19,99,13.8,1
        9,8,19,20.1,1
        10,NA,194,NULL,n/a
        """,
}

# FIXTURES

@pytest.fixture(scope='session')
def data_examples():
    return {k: pd.read_csv(StringIO(v), index_col=0) for k, v
            in STR_DATA_EXAMPLES.items()}


@pytest.mark.slow
@pytest.fixture(scope='session')
def fake_regression_data():
    """Returns Pandas DataFrame of fake regression data of size 500
    generated by the following data generating process:

    x1 ~ Normal(0, 1)
    x2 ~ Binomial(0.5)
    x3 ~ Exponential(10)
    x4 ~ Poisson(10)
    y = x1 + x2 + x3 + x4 + Normal(0, 1)
    """

    N = 500
    np.random.seed(42)
    x1 = np.random.normal(size=N)
    x2 = np.random.binomial(n=N, p=0.5)
    x3 = np.random.exponential(scale=10.0, size=N)
    x4 = np.random.poisson(lam=10, size=N)
    y = x1 + x2 + x3 + x4 + np.random.normal(size=N)

    data = pd.DataFrame({
        'x1': x1,
        'x2': x2,
        'x3': x3,
        'x4': x4,
        'y': y
    })

    return data


# UNIT TESTS

def test_column_wrangler():
    """Columns are transformed into a consistent format.
    """
    data = pd.DataFrame({
        'column1': [1, 2, 3],
        'cOLUmn2': [1, 2, 3],
        '    cOLUmn3 ': [1, 2, 3],
        ' column  4 ': [1, 2, 3],
    })
    result = _column_wrangler(data).columns
    expected = pd.Index(['column1', 'column2', 'column3', 'column_4'])
    assert_index_equal(result, expected)


def test_obj_wrangler(data_examples):
    """Columns with `object` dtype are converted to `StringDtype`.
    """
    data = data_examples['iraq_vote']
    result = _obj_wrangler(data)
    result_cols = (result.select_dtypes(include=['string'])
                         .columns)
    expected = pd.Index(['state.abb', 'name', 'state.name'])  # String columns
    assert_index_equal(result_cols, expected)


if __name__ == "__main__":
    pass