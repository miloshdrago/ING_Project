import pytest

import numpy as np
import pandas as pd

# Adjust location of module relatime to test file
from Seasonality_adjustment import Seasonality



def test_time_values():
    # Adjust location of file relatime to test module
    filename = "seasonality_values.csv"
    time_value_1 = 150000
    expected_1 = 0.9
    time_value_2 = 20000
    expected_2 = 0.16

    season = Seasonality(filename)

    actual_1 = season.scale(time_value_1)
    assert actual_1 == expected_1 ,"Expected {0}, got {1}".format(expected_1, actual_1)

    actual_2 = season.scale(time_value_2)
    assert actual_2 == expected_2 ,f"Expected {expected_2}, got {actual_2}"

def test_time_more_than_seasonaolity_file():
    # Adjust location of file relatime to test module
    filename = "seasonality_values.csv"
    time_value = 150000 + 601200
    expected = 0.9

    season = Seasonality(filename)

    actual = season.scale(time_value)
    assert actual == expected ,"Expected {0}, got {1}".format(expected, actual)
