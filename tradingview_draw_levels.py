import TradingviewHelper
import json
from time import sleep
import sys
import yaml

# Script takes two arguments: arg1=1 will delete all lines and price ranges first, arg2=1 will plot levels.
delta_es_spx = 5.75  # must be adjusted daily based on difference between ES and SPX
delta_es_spy = 12  # must be adjusted daily based on difference between ES and 10*SPY
sleep_time_for_recaptcha = 10  # Seconds
with open('config.yaml', 'r') as f:
    config_yaml = yaml.safe_load(f)
print('sys.argv=', sys.argv)

tradingview_helper = TradingviewHelper.TradingviewHelper()
sleep(sleep_time_for_recaptcha)  # Added a ton of delay here because often tradingview will prompt for recaptcha to weed out bots, user intervention is required here. If not getting recaptcha, this delay can be commented out
tradingview_helper.open_chart(config_yaml['charts']['es'])  # ES daytrade chart

if sys.argv[1] == '1':
    print('Deleting all lines and price ranges...')
    tradingview_helper.delete_all_lines_and_price_ranges()

if sys.argv[2] == '1':
    print('Drawing levels and ranges on chart...')
    # Load Json file with levels and price ranges
    jsonn = json.load(open('es.json'))
    # Draw Levels
    if 1:
        levels_support = jsonn['levels_support']
        levels_resistance = jsonn['levels_resistance']
        labels_levels_support = jsonn['labels_levels_support']
        labels_levels_resistance = jsonn['labels_levels_resistance']
        for idx in range(len(levels_support)):
            tradingview_helper.draw_horizontal_line(levels_support[idx], template='support', label=labels_levels_support[idx])
        for idx in range(len(levels_resistance)):
            tradingview_helper.draw_horizontal_line(levels_resistance[idx], template='resistance', label=labels_levels_resistance[idx])

    # Draw Ranges
    if 1:
        ranges_support = jsonn['ranges_support']
        ranges_resistance = jsonn['ranges_resistance']
        labels_ranges_support = jsonn['labels_ranges_support']
        labels_ranges_resistance = jsonn['labels_ranges_resistance']
        for idx in range(len(ranges_support)):
            tradingview_helper.draw_horizontal_line(ranges_support[idx][0], 'support', labels_ranges_support[idx])
            tradingview_helper.draw_price_range(ranges_support[idx][0],ranges_support[idx][1],'support')

        for idx in range(len(ranges_resistance)):
            tradingview_helper.draw_horizontal_line(ranges_resistance[idx][0], 'resistance', labels_ranges_resistance[idx])
            tradingview_helper.draw_price_range(ranges_resistance[idx][0],ranges_resistance[idx][1],'resistance')

flag = input('save_chart? y/n:')
if str(flag).lower() == 'y':
    tradingview_helper.save_chart()
    tradingview_helper.quit()
