# pytv

Scripts written and tested for py3.10 on windows only

Additional modules you might need to install:
pyyaml
selenium
undetected_chromedriver

Download chromedriver.exe file, and have chrome browser updated to latest
https://chromedriver.chromium.org/downloads




**For tradingview_draw_levels.py:**

Update login_details.py with tradingview login credentials, or modify the TradingViewHelper.py module to take input for password at prompt if you don't want to store credentials in local file.

Tradingview likes to activate recaptcha if you login too many times, so there is a delay in the script to account for this at login screen.

Update the pyyaml file with the link to your tradingview chart

You will need to add 'support'/'resistance' templates to tradingview horizontal line and price range. They can be called whatever you want, but the templates need to match what is passed from the main script to TradingViewHelper.py




**For levels_parser_mancini.py**

Update login_details.py with substack login credentials, or modify the levels_parser_mancini.py module to take input for password at prompt if you don't want to store credentials in local file.

The format for support and resistance text is:

Supports are: 3950, 4000, 3910-3915 (major), 3920-3925 (major).

Resistances are: 4100, 4150, 4115-4120 (major), 4130-4135 (major).

I am not very good at regex, so no commas supported inside the labels, semicolons are ok i.e. can say (major; knife catch) but not (major, knife catch)



The source are completely open, make them yours, no licenses attached.
