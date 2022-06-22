import json

import pandas as pd
import numpy as np
import plotly.express as px
pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.width = None

time_frame = 'H4'
instrument = 'SP500'
type_of_instrument = 'INDICES'  # CRYPTO, FOREX, INDICES or ENERGY
data_source = 'FOREXSB'  #  FOREXSB, NINJATRADER, YAHOO


# Open csv file and create data frame
csv_path = f'C:\\Users\\48515\\PycharmProjects\\CSV_DATA\\{type_of_instrument}\\{instrument}\\{data_source}\\'
csv_name = f'{instrument}_{time_frame}.csv'
full_path = csv_path + csv_name
df = pd.read_csv(full_path, delimiter='\t')


output_file_name = f'{instrument} - {time_frame} DATA'
output_file_path = f'C:\\Users\\48515\\PycharmProjects\\JSON_DATA\\{type_of_instrument}\\{instrument}\\{data_source}\\'
full_output_file_path = output_file_path + output_file_name
json_file = open(full_output_file_path + ".json", 'w')



# Spliting data and time
split_time = df['Time'].str.split(' ', n=1, expand=True)
df['Year_month_day']= (split_time[0])
df['Minutes']= (split_time[1])
split_hour_min_sec = df['Minutes'].str.rsplit(':', n=2, expand=True)
hour_min = split_hour_min_sec[0] + ':' + split_hour_min_sec[1]
split_day = df['Year_month_day'].str.rsplit('-', n=1, expand=True)

# Splitting Day
df['Day']= (split_day[1])

# Splitting Month from Year
df['Year-Month']= (split_day[0])
split_month = df['Year-Month'].str.rsplit('-', n=1, expand=True)
year = split_month[0]
month = split_month[1]
to_list = month.to_list()
month_split_list = []
for month in to_list:
    digit_split_list = []
    for digit in month:
        digit_split_list.append(digit)
    month_split_list.append(digit_split_list)
for month in month_split_list:
    if month[0] == '0':
        month[0] = ''
to_list = []
for month in month_split_list:
    new_month_string = ''
    for digit in month:
        new_month_string = new_month_string + digit
    to_list.append(new_month_string)

# Resetting Year Month Column
df['Year-Month']= year + '-' + to_list + '-' + (split_day[1]) + ' ' + hour_min


# Reordering columns and selecting what I want in the data frame
df = df[['Year-Month', 'Day', 'Open', 'High', 'Low', 'Close']]


#-------------------DATA START AND STOP DATES--------------

amount_of_data = 100000
df_0_3 = df[7000:amount_of_data]  #  Setting dataframe to...

#print number of rows:
print(df_0_3.head(3))



# Getting all indexs of data frame
indexs_of_DF = df_0_3.index

main_list = []
day_list = []

# for row in data frame using index value
for i in indexs_of_DF:
    month = df_0_3.at[i, 'Year-Month']
    day = df_0_3.at[i, 'Day']
    d_open = df_0_3.at[i, 'Open']
    d_high = df_0_3.at[i, 'High']
    d_low = df_0_3.at[i, 'Low']
    d_close = df_0_3.at[i, 'Close']
    daily_ohlc = {"open": d_open, "high": d_high, "low": d_low, "close": d_close}
    daily_key_value = {month: daily_ohlc}

    # going through each index day by seeing if the month changed
    # only used once since it's the first index
    if i == 0:
        main_list.append(daily_key_value)

    # going through each index day by seeing if the month changed
    if i > 0:
        main_list.append(daily_key_value)




main_list_string = json.dumps(main_list)
main_list_json = json.loads(main_list_string)
# Write json to file
json.dump(main_list_json, json_file, indent=4)

json_file.close()