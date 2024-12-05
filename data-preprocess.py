# import the necessary libraries
import pandas as pd
from utils.pre_processing_functions import encode_sub_type, convert_build_condition, encode_kitchen, get_latitude, get_longitude, get_distance

df = pd.read_csv('../immo_eliza_analysis/cleaned-data.csv')

# Drop unecessaty columns
df.drop(['bedroom_nr', 'swimming_pool', 'furnished', 'open_fire', 'sub_property_group_encoded'], axis=1, inplace=True)

# Drop observations under "other" type of property.
other_properties = df[df['subtype_of_property'].isin(['other property', 'mixed use building', ])].index
df.drop(other_properties, inplace=True)

# Make dictionary to ecode property subtype
sub_types_dict = {'kot': 0,
'chalet': 1,
'flat studio' : 2,
'service flat': 3,
'bungalow': 4,
'town house': 5,
'ground floor': 6,
'apartment': 7,
'house': 8,
'triplex': 9,
'farmhouse': 10,
'loft': 11,
'duplex': 12,
'apartment block': 13,
'country cottage': 14,
'penthouse': 15,
'mansion': 16,
'villa': 17,
'exceptional property': 18,
'manor house': 19,
'castle': 20}

# Apply encode subtype function and convert values to int
df['subtype_ecoded'] = df['subtype_of_property'].apply(lambda x: encode_sub_type(x, sub_types_dict))
df['subtype_ecoded'] = df['subtype_ecoded'].astype(int)

# Drop unknown building condition rows:
unknown_building_state = df[df['building_condition'] == 'no info'].index
df.drop(unknown_building_state, inplace=True)

# Apply function to convert building condition to numberic
df['building_condition'] = df['building_condition'].apply(convert_build_condition)

# Remove apartments with 5 facades
drop_by_facades = df[(df['facade_number'] > 4) & (df['type_of_property'] == 0)].index
df.drop(drop_by_facades, inplace=True)

# change it to numerical values
df['equipped_kitchen'] = df['equipped_kitchen'].apply(encode_kitchen)

# drop houses without plot size
zero_plot_surface = df[(df['type_of_property'] == 1) & (df['plot_surface'] == 0)]

# drop the 'plot_surface' column.
df.drop('plot_surface', axis=1, inplace=True)


# Feature engineering - Add distance to province capital
# import zip codes data
zip_codes_df = pd.read_csv('utils/zipcode_belgium.csv')

# rearange df
zip_codes_df.index = zip_codes_df.index + 1  # Shift all other rows down
zip_codes_df.loc[0] = zip_codes_df.columns # Add info for Brussels, beacuase it is incorrectly used at the column names in the original csv file.

# Correct column names
column_names = ['zip_code_col', 'commune', 'longitude', 'latitude']
zip_codes_df = zip_codes_df.sort_index()
zip_codes_df.columns = column_names

# Correct data type of the columns, because it caused error to function
zip_codes_df['zip_code_col'] = zip_codes_df['zip_code_col'].astype(int)
zip_codes_df['latitude'] = zip_codes_df['latitude'].astype(float)
zip_codes_df['longitude'] = zip_codes_df['longitude'].astype(float)


# Add latitude and logitude to all observations
df['latitude'] = df['zip_code'].apply(lambda x: get_latitude(x, zip_codes_df))
df['longitude'] = df['zip_code'].apply(lambda x: get_longitude(x, zip_codes_df))

# create data frame with latitude and longitude for each provice capital
provinces = [
['West-Vlaanderen', 'Oost-Vlaanderen', 'Antwerpen', 'Liège', 'Vlaams Brabant', 'Hainaut', 'Brabant Wallon', 'Namur', 'Luxembourg', 'Limburg', 'Bruxelles'],
[51.2085, 51.05, 51.2199, 50.6402, 50.8791, 60.3913, 50.7154, 50.4649, 49.6116, 50.9305, 50.8477],
[3.2251, 3.7304, 4.415, 5.5689, 4.7025, 5.3221, 4.6177, 4.865, 6.1319, 5.3324, 4.3572]
 ]    
col_names = ['province', 'latitude', 'longitude']
provinces_df = pd.DataFrame(provinces).T
provinces_df.columns = col_names
provinces_df['latitude'] = provinces_df['latitude'].astype(float)
provinces_df['longitude'] = provinces_df['longitude'].astype(float)

# calculate distance of each property to the provice capital and add as a new feature
df['km_to_capital'] = df.apply(lambda row: get_distance(row, provinces_df), axis=1)


# drop cols that are no longer needed
df.drop(['subtype_of_property', 'zip_code', 'commune', 'province', 'latitude', 'longitude'], axis=1, inplace=True)

# save processed data to a new csv file
df.to_csv('ml_data.csv', index=False)