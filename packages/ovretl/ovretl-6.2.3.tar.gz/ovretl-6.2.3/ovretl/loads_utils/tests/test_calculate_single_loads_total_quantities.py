import numpy as np
import pandas as pd
from ovretl.loads_utils.calculate_single_load_total_quantities import calculate_single_load_total_quantities
from pandas.util.testing import assert_frame_equal


def test_calculate_single_loads_total_quantities():
    loads_df = pd.DataFrame(
        data={
            "unit_weight": [10, 100, 10, 10],
            "unit_length": [120, 120, 120, 120],
            "unit_height": [100, 100, 100, 100],
            "unit_width": [80, 80, 80, 80],
            "unit_number": [1, 1, 1, 1],
            "total_weight_in_kg": [200, np.nan, 200, 200],
            "total_weight_in_lbs": [440.92, np.nan, 440.92, 440.92],
            "total_volume_in_cbcm": [900000, 900000, 1000000, np.nan],
            "total_volume_in_cbin": [54911.53, 54911.53, 61012.81, np.nan],
        }
    )
    loads_df_with_total_quantities = pd.DataFrame(
        data={
            "unit_weight": [10, 100, 10, 10],
            "unit_length": [120, 120, 120, 120],
            "unit_height": [100, 100, 100, 100],
            "unit_width": [80, 80, 80, 80],
            "unit_number": [1, 1, 1, 1],
            "total_weight_in_kg": [200, 100, 200, 200],
            "total_weight_in_lbs": [440.92, 220.46, 440.92, 440.92],
            "total_volume_in_cbm": [0.9, 0.9, 1, 0.96],
            "total_volume_in_cbf": [31.78, 31.78, 35.31, 0.03],
            "total_number": [1, 1, 1, 1],
        }
    )
    loads_df = loads_df.apply(calculate_single_load_total_quantities, axis=1)
    loads_df = loads_df.drop(columns=["total_volume_in_cbcm", "total_volume_in_cbin"]).reset_index(drop=True)
    assert_frame_equal(loads_df, loads_df_with_total_quantities, check_dtype=False)
