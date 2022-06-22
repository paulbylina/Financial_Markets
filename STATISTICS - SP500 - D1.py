from datetime import datetime
import time
import json


# -------------FILL IN VARIABLES:
date = "6-19-2022"
instrument_used = "SP500"
time_frame = 'D1'
data_source = 'FOREXSB'  # YAHOO, FOREXSB, NINJATRADER
# --------------------------------


# -------------------CONSTANTS
statistic_name = f"STATISTICS_{instrument_used}_{time_frame}"
json_data_path_base = f'C:\\Users\\48515\\PycharmProjects\\JSON_DATA\\INDICES\\SP500\\{data_source}\\'
json_data_name = f'{instrument_used} - {time_frame} DATA.json'
full_json_data_path = json_data_path_base + json_data_name
# Output file
output_dir = f"C:\\Users\\48515\\PycharmProjects\\STATISTICS\\INDICES\\SP500\\{data_source}\\{time_frame}\\"
file_name = statistic_name + '_' + date + '.txt'
full_output_path = output_dir + file_name
# -----------------------------



# IMPORTING JSON FILES
with open(full_json_data_path) as x:
  D1_json = json.load(x)

# UP/DOWN BAR COUNTERS
bull_candle_counter = 0
bear_candle_counter = 0

# OPEN TO CLOSE RANGE LIST
oc_bull_range_list = []
oc_bear_range_list = []

# High to low RANGE LIST
hl_bull_range_list = []
hl_bear_range_list = []

# High to low RANGE LIST
o_h_range_list = []
o_l_range_list = []

# Data counter
data_counter = 0

# -----------------------------START PROGRAM-------------------------------
for D1_candle in D1_json:
    # INITIALIZING DATA COUNTER
    data_counter = data_counter + 1

    for key in D1_candle:
        # O-H-L-C Variables
        daily_open = D1_candle[key]['open']
        daily_high = D1_candle[key]['high']
        daily_low = D1_candle[key]['low']
        daily_close = D1_candle[key]['close']


        # Non candle specific data
        o_h_range = daily_high - daily_open
        o_l_range = daily_open - daily_low
        # Appending to lists
        o_h_range_list.append(o_h_range)
        o_l_range_list.append(o_l_range)


        if daily_close > daily_open:
            # counting bull candles
            bull_candle_counter = bull_candle_counter + 1

            # open-close range
            oc_bull_range = daily_close - daily_open
            # high-low range
            hl_bull_range = daily_high - daily_low

            # Appending to lists
            oc_bull_range_list.append(oc_bull_range)
            hl_bull_range_list.append(hl_bull_range)

        if daily_close < daily_open:
            # counting bear candles
            bear_candle_counter = bear_candle_counter + 1

            # open-close range
            oc_bear_range = daily_open - daily_close
            # high-low range
            hl_bear_range = daily_high - daily_low


            # Appending to list
            oc_bear_range_list.append(oc_bear_range)
            hl_bear_range_list.append(hl_bear_range)



# ------------------------------END PROGRAM--------------------------------
# ------------------Create final variables for statistics------------------

# getting sum of list of daily ranges
oc_bull_range_sum = sum(oc_bull_range_list)
oc_bear_range_sum = sum(oc_bear_range_list)

hl_bull_range_sum = sum(hl_bull_range_list)
hl_bear_range_sum = sum(hl_bear_range_list)

o_h_range_sum = sum(o_h_range_list)
o_l_range_sum = sum(o_l_range_list)


# total sum of both bull and bear candles
oc_bull_bear_sum = oc_bull_range_sum + oc_bear_range_sum
hl_bull_bear_sum = hl_bull_range_sum + hl_bear_range_sum

total_candles = bull_candle_counter + bear_candle_counter

bull_percentage = ((bull_candle_counter / total_candles) * 100)
bear_percentage = ((bear_candle_counter / total_candles) * 100)

# Average daily ranges
oc_average_daily_range = (oc_bull_bear_sum / total_candles) / 0.25  # minimum fluctuation ticks for sp500 futures is 1/4 of a point
hl_average_daily_range = (hl_bull_bear_sum / total_candles) / 0.25  # minimum fluctuation ticks for sp500 futures is 1/4 of a point
o_h_average = (o_h_range_sum / data_counter) / 0.25
o_l_average = (o_l_range_sum / data_counter) / 0.25





# --------------------------PRINTED RESULTS:----------------------------------
print("NAME: " + statistic_name)
print("DATE: " + date)
print("INSTRUMENT: " + instrument_used)
print("TIME FRAME: " + time_frame)
print("AMOUNT OF DATA: " + str(data_counter))

# print("AMOUNT OF BULL CANDLES: " + str(bull_candle_counter))
print("% OF BULL CANDLES: " + str('%.2f' % bull_percentage) + ' %')
# print("AMOUNT OF BEAR CANDLES: " + str(bear_candle_counter))
print("% OF BEAR CANDLES: " + str('%.2f' % bear_percentage) + ' %')

print("SUM OF BULL CANDLES - Open-Close: " + str('%.2f' % oc_bull_range_sum))
print("SUM OF BEAR CANDLES - Open-Close: " + str('%.2f' % oc_bear_range_sum))
print("AVG BULL CANDLE - Open-Close: " + str('%.2f' % hl_bear_range_sum))
print("AVG BEAR CANDLE - Open-Close: " + str('%.2f' % hl_bear_range_sum))

print("Open-High: " + str('%.2f' % o_h_range_sum))
print("Open-Low: " + str('%.2f' % o_l_range_sum))
print("AVG Open-High: " + str('%.2f' % o_h_average))
print("AVG Open-Low: " + str('%.2f' % o_l_average))







print("AVERAGE DAILY RANGE - Open-Close (in ticks): " + str('%.2f' % oc_average_daily_range))
print("AVERAGE DAILY RANGE - High-Low (in ticks): " + str('%.2f' % hl_average_daily_range))


# ---------------------------OUTPUT RESULTS FILE---------------------------



save_results = open(full_output_path, 'w')

save_results.write("NAME: " + statistic_name + '\n')
save_results.write("DATE: " + date + '\n')
save_results.write("INSTRUMENT: " + instrument_used + '\n')
save_results.write("TIME FRAME: " + time_frame + '\n')
save_results.write("AMOUNT OF DATA: " + str(data_counter) + '\n')

save_results.write("AMOUNT OF BULL CANDLES: " + str(bull_candle_counter) + '\n')
save_results.write("% OF BULL CANDLES: " + str('%.2f' % bull_percentage) + ' %' + '\n')
save_results.write("AMOUNT OF BEAR CANDLES: " + str(bear_candle_counter) + '\n')
save_results.write("% OF BEAR CANDLES: " + str('%.2f' % bear_percentage) + ' %' + '\n')

save_results.write("SUM OF BULL CANDLES - Open-Close: " + str('%.2f' % oc_bull_range_sum) + '\n')
save_results.write("SUM OF BULL CANDLES - High-Low: " + str('%.2f' % hl_bull_range_sum) + '\n')
save_results.write("SUM OF BEAR CANDLES - Open-Close: " + str('%.2f' % oc_bear_range_sum) + '\n')
save_results.write("SUM OF BEAR CANDLES - High-Low: " + str('%.2f' % hl_bear_range_sum) + '\n')

save_results.write("AVERAGE DAILY RANGE - Open-Close (in ticks): " + str('%.2f' % oc_average_daily_range) + '\n')
save_results.write("AVERAGE DAILY RANGE - High-Low (in ticks): " + str('%.2f' % hl_average_daily_range))

save_results.close()