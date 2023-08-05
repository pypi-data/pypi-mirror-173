import pandas as pd


def calculate_single_load_total_weight_in_kg(single_load):
    return single_load["unit_weight"] * single_load["unit_number"]


def calculate_single_load_total_volume_in_cbm(single_load):
    return (
        single_load["unit_length"]
        * single_load["unit_width"]
        * single_load["unit_height"]
        * single_load["unit_number"]
        / 1000000
    )


def calculate_single_load_total_quantities(single_load: pd.Series) -> pd.Series:
    single_load["total_weight_in_kg"] = (
        single_load["total_weight_in_kg"]
        if not pd.isna(single_load["total_weight_in_kg"]) and single_load["total_weight_in_kg"] > 0
        else calculate_single_load_total_weight_in_kg(single_load)
    )
    single_load["total_weight_in_lbs"] = (
        single_load["total_weight_in_lbs"]
        if not pd.isna(single_load["total_weight_in_lbs"]) and single_load["total_weight_in_lbs"] > 0
        else round(single_load["total_weight_in_kg"] / 0.4536, 2)
    )
    single_load["total_volume_in_cbm"] = (
        single_load["total_volume_in_cbcm"] / 1000000
        if not pd.isna(single_load["total_volume_in_cbcm"]) and single_load["total_volume_in_cbcm"] > 0
        else calculate_single_load_total_volume_in_cbm(single_load)
    )
    single_load["total_volume_in_cbf"] = (
        round(single_load["total_volume_in_cbin"] / 1728, 2)
        if not pd.isna(single_load["total_volume_in_cbin"]) and single_load["total_volume_in_cbin"] > 0
        else round(single_load["total_volume_in_cbm"] / 35.3147, 2)
    )
    single_load["total_number"] = single_load["unit_number"]
    return single_load


def calculate_taxable_weight(total_weight: float, total_volume: float):
    return round(max(total_volume / 6, total_weight / 1000) * 1000, 3)


def calculate_weight_measurable(total_weight: float, total_volume: float):
    return round(max(total_weight / 1000, total_volume, 1), 3)
