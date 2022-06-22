from datetime import datetime
import time
import json
import statistics
from statistics import mode

# OPTIONS:
date = "3/20/2022"
instrument_used = "SP500"
market = 'INDICES'  # CRYPTO, FOREX, INDICES or ENERGY
time_frame_base = 'D1'
time_frame_daily = 'D1'
time_frame_monthly = 'Monthly'
time_frame_yearly = 'Yearly'
data_source = 'YAHOO'  #  NINJATRADER, FOREXSB, YAHOO
strategy_name = "BREAKOUT - "
json_list = 'LIST'
json_dict = 'DICTIONARY'
pre_loop_on = True
start_date = '2012-01-03'
current_instrument_price = 4463.0  #  Used to calculate ticks per trade
tick_fluc = 4
work_days_per_year = 261

# Base time frame directory
json_data_path_base = f'C:\\Users\\48515\\PycharmProjects\\JSON_DATA\\{market}\\{instrument_used}\\{data_source}\\{json_dict}\\'
json_data_name_base = f'{instrument_used} - {time_frame_base}_DATA.json'
full_json_data_path_base = json_data_path_base + json_data_name_base

# Daily time frame directory
json_data_path_daily = f'C:\\Users\\48515\\PycharmProjects\\JSON_DATA\\{market}\\{instrument_used}\\{data_source}\\{json_dict}\\'
json_data_name_daily = f'{instrument_used} - {time_frame_daily}_DATA.json'
full_json_data_path_daily = json_data_path_daily + json_data_name_daily

# Monthly time frame directory
json_data_path_monthly = f'C:\\Users\\48515\\PycharmProjects\\JSON_DATA\\{market}\\{instrument_used}\\{data_source}\\{json_dict}\\'
json_data_name_monthly = f'{instrument_used} - {time_frame_monthly}_DATA.json'
full_json_data_path_monthly = json_data_path_monthly + json_data_name_monthly

# Yearly time frame directory
json_data_path_yearly = f'C:\\Users\\48515\\PycharmProjects\\JSON_DATA\\{market}\\{instrument_used}\\{data_source}\\{json_dict}\\'
json_data_name_yearly = f'{instrument_used} - {time_frame_yearly}_DATA.json'
full_json_data_path_yearly = json_data_path_yearly + json_data_name_yearly


# IMPORTING JSON FILES:

#  Base json
with open(full_json_data_path_base) as x:
  base_tf_json = json.load(x)
#  Daily json
with open(full_json_data_path_daily) as x:
  daily_tf_json = json.load(x)
#  Monthly json
with open(full_json_data_path_monthly) as y:
  monthly_tf_json = json.load(y)
#  Yearly json
with open(full_json_data_path_yearly) as z:
  yearly_tf_json = json.load(z)


# -----------------------------START PROGRAM D1/MONTHLY---------------------------

# Data counter
data_counter = 0
# To get start and end dates create list
date_list = []
# Profit/Loss
long_trade_pnl_list = []
short_trade_pnl_list = []
# Trade counter
trade_counter = 0
pre_loop_counter = 0

for year_month_day in daily_tf_json:
    # splitting date
    date_split = year_month_day.split('-')
    year = date_split[0]
    month = date_split[1]
    day = date_split[2]
    daily_index = list(daily_tf_json.keys()).index(year_month_day)
    prev_day_index = daily_index - 1
    start_index = list(daily_tf_json.keys()).index(start_date)
    # Print counter option
    if pre_loop_on == True:
        pre_loop_counter = pre_loop_counter + 1
        print('Counter: ', pre_loop_counter)

    if daily_index >= start_index:
        # Counting days
        data_counter = data_counter + 1
        date_list.append(year_month_day)

        daily_open = daily_tf_json[year_month_day]['open']
        daily_high = daily_tf_json[year_month_day]['high']
        daily_low = daily_tf_json[year_month_day]['low']
        daily_close = daily_tf_json[year_month_day]['close']

        prev_day_date = list(daily_tf_json)[prev_day_index]
        prev_day_open = daily_tf_json[prev_day_date]['open']
        prev_day_high = daily_tf_json[prev_day_date]['high']
        prev_day_low = daily_tf_json[prev_day_date]['low']
        prev_day_close = daily_tf_json[prev_day_date]['close']

        # Getting previous months date
        if month == '01':
            prev_month_year = int(year) - 1
            prev_month_date = str(prev_month_year) + '-' + '12'
        if month == '02':
            prev_month_date = year + '-' + '01'
        if month == '03':
            prev_month_date = year + '-' + '02'
        if month == '04':
            prev_month_date = year + '-' + '03'
        if month == '05':
            prev_month_date = year + '-' + '04'
        if month == '06':
            prev_month_date = year + '-' + '05'
        if month == '07':
            prev_month_date = year + '-' + '06'
        if month == '08':
            prev_month_date = year + '-' + '07'
        if month == '09':
            prev_month_date = year + '-' + '08'
        if month == '10':
            prev_month_date = year + '-' + '09'
        if month == '11':
            prev_month_date = year + '-' + '10'
        if month == '12':
            prev_month_date = year + '-' + '11'

        # Previous month OHLC data:
        prev_month_open = monthly_tf_json[prev_month_date]['open']
        prev_month_high = monthly_tf_json[prev_month_date]['high']
        prev_month_low = monthly_tf_json[prev_month_date]['low']
        prev_month_close = monthly_tf_json[prev_month_date]['close']

        # TRADE CONDITION:
            # LONG:
        if prev_day_high >= prev_month_high:
            if daily_high >= prev_day_high:
                long_trade_pnl = daily_close - prev_day_high
                long_trade_percent = long_trade_pnl / daily_open
                long_trade_pnl_list.append(long_trade_percent)
                trade_counter = trade_counter + 1
        # TRADE CONDITION:
            # SHORT:
        if prev_day_low <= prev_month_low:
            if daily_low <= prev_day_low:
                short_trade_pnl = prev_day_low - daily_close
                short_trade_percent = short_trade_pnl / daily_open
                short_trade_pnl_list.append(short_trade_percent)
                trade_counter = trade_counter + 1

# Creating start and end date variables
start_date = date_list[0]
end_date = date_list[-1]

# Get Profit/loss
total_long_pnl = sum(long_trade_pnl_list)
total_short_pnl = sum(short_trade_pnl_list)
total_pnl = total_long_pnl + total_short_pnl
per_trade_pnl = total_pnl / trade_counter
total_pnl = round((total_pnl * current_instrument_price), 2) * tick_fluc
per_trade_pnl = round((per_trade_pnl * current_instrument_price), 2) * tick_fluc

# Get % of trade taken
percent_trades_taken = trade_counter / data_counter

# Total ticks per year
days_traded = work_days_per_year * percent_trades_taken
ticks_per_year = round(days_traded * per_trade_pnl, 0)
days_traded = round(work_days_per_year * percent_trades_taken, 0)

# Output file
output_dir = f"C:\\Users\\48515\\PycharmProjects\\STRATEGY_RESULTS\\{market}\\{instrument_used}\\{data_source}\\"
strategy_name = strategy_name + time_frame_base + '_' + time_frame_monthly + ' - ' + start_date + '_' + end_date + '.txt'
full_output_path = output_dir + strategy_name

# -----------------------END PROGRAM D1/MONTHLY-------------------------------

# --------------------------PRINTED RESULTS:----------------------------------
print("STRATEGY: " + strategy_name)
print("DATE: " + date)
print("INSTRUMENT: " + instrument_used)
print("DATA SOURCE: " + str(data_source))
print("DATA START DATE: " + start_date)
print("AMOUNT OF DAYS: " + str(data_counter))
print("TOTAL TRADES: " + str(trade_counter))
print("TRADES TAKEN %: " + str(round(percent_trades_taken * 100, 1)) + ' %')
print("DATA END DATE: " + end_date)
print("TOTAL PROFIT/LOSS: " + str(total_pnl) + ' ticks')
print("PER TRADE PROFIT/LOSS: " + str(per_trade_pnl) + ' ticks')
print("DAYS TRADED PER YEAR: " + str(days_traded) + '/' + str(work_days_per_year))
print("TICKS PER YEAR: " + str(ticks_per_year))

# ---------------------------OUTPUT RESULTS FILE---------------------------
save_results = open(full_output_path, 'w')

save_results.write("STRATEGY:  " + strategy_name + '\n')
save_results.write("DATE: " + date + '\n')
save_results.write("INSTRUMENT: " + instrument_used + '\n')
save_results.write("DATA SOURCE: " + str(data_source) + '\n')
save_results.write("DATA START DATE: " + start_date + '\n')
save_results.write("DATA END DATE: " + end_date + '\n')
save_results.write("AMOUNT OF DAYS: " + str(data_counter) + '\n')
save_results.write("TOTAL TRADES: " + str(trade_counter) + '\n')
save_results.write("TRADES TAKEN %: " + str(round(percent_trades_taken * 100, 1)) + ' %' + '\n')
save_results.write("TOTAL PROFIT/LOSS: " + str(total_pnl) + ' Ticks' + '\n')
save_results.write("PER TRADE PROFIT/LOSS: " + str(per_trade_pnl) + ' Ticks' + '\n')
save_results.write("DAYS TRADED PER YEAR: " + str(days_traded) + '/' + str(work_days_per_year) + '\n')
save_results.write("TICKS PER YEAR: " + str(ticks_per_year))

save_results.close()