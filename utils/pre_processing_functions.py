# import pandas as pd
from math import radians, sin, cos, sqrt, atan2


# Function to encode property subtype
def encode_sub_type(subtype_of_property, sub_types_dict):
    if subtype_of_property in sub_types_dict.keys():
        subtype_of_property = sub_types_dict[subtype_of_property]
    return subtype_of_property


# Function to convert build condition to ordinal
def convert_build_condition(building_condition) -> int:
    """
    Converts string from 'bulding_condition' column
    to an ordinal value.

    PARAMS:
    building_condition -str: string corresponding to 'to resote', 'to renovate' or 'good'

    RETURNS:
    0 - int: if state is 'to restore'.
    1 - int: if state is 'to renovate'.
    2 - int: if state is 'good'.
    """

    if building_condition == "to restore":
        return 0
    elif building_condition == "to renovate":
        return 1
    else:
        return 2


# Function to encode the kitchen's state of the property
def encode_kitchen(kitchen_state) -> int:
    """
    Transforms state of the property's kitchen to an ordinal numeric value

    PARAMS:
    kitchen_state -str: string kitchen status

    RETURNS
    0, 1, 2: if 'not installed', 'installed' or 'equipped' respectively
    """
    if kitchen_state == "not installed":
        return 0
    elif kitchen_state == "installed":
        return 1
    else:
        return 2


# Function to extract latitude from zip code df
def get_latitude(zip_code, zip_codes_df):
    """
    Assigns the latitude to a given observation.

    PARAMS:
    zip_code - int: zip_code where the property is located
    zip_codes_df - pandas data frame: where the latitude is to be found

    RETURNS
    latitude -float: latitude of the observation
    """
    row = zip_codes_df[zip_codes_df["zip_code_col"] == zip_code]
    latitude = row["latitude"].values[0]

    return latitude


# Function to extract longitude from zip code df
def get_longitude(zip_code, zip_codes_df):
    """
    Assigns the longitude to a given observation.

    PARAMS:
    zip_code - int: zip_code where the property is located
    zip_codes_df - pandas data frame: where the longitude is to be found

    RETURNS
    longitude -float: latitude of the observation
    """
    row = zip_codes_df[zip_codes_df["zip_code_col"] == zip_code]
    longitude = row["longitude"].values[0]
    return longitude


# Function to calculate distance to the province's capital
def get_distance(row, provinces_df):
    """
    Calculate the distance between two points on the Earth's surface.

    PARAMS:
    row -df slice: row to calculate the distance for.
    provinces_df - df: df containing the latitude and logitude for each province

    RETURN
    Distance in kilometers, rounded to two decimal points
    """
    lat1 = row["latitude"]
    lon1 = row["longitude"]

    row_province = row["province"]

    province_data = provinces_df[provinces_df["province"] == row_province]

    lat2 = province_data["latitude"].values[0]
    lon2 = province_data["longitude"].values[0]

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Earth's radius in kilometers
    radius_of_earth_km = 6371

    # Calculate distance
    distance = round(radius_of_earth_km * c, 2)
    return distance


def remove_outliers(df, lower_ptc, upper_ptc):
    """
    Removes outliers from a dataframe according to the given percentage
    limits of the lower and upper quantile limits.

    PARAMS:
    df -DataFrame: the dataframe from which outliers are to be removed.
    lower_ptc -float: the percentage for the lower limit.
    upper_prc -float: the percentage for the upper limit.

    RETURNS
    df - The updated dataframe
    """
    for col in df:
        Q1 = df[col].quantile(lower_ptc)
        Q3 = df[col].quantile(upper_ptc)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    return df
