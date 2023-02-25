# pytv

Script written and tested for py3.10

Additional modules you will likely need to install:
pyyaml
selenium

Download chromedriver.exe file, and have chrome browser updated to latest
https://chromedriver.chromium.org/downloads

Update login_details.py with tradingview login credentials, or modify the TradingViewHelper.py module to take input for password at prompt if you don't want to store credentials in local file.

Tradingview likes to activate recaptcha if you login too many times, so there is a delay in the script to account for this at login screen.

Update the pyyaml file with the link to your tradingview chart

You will need to add 'support'/'resistance' templates to tradingview horizontal line and price range. They can be called whatever you want, but the templates need to match what is passed from the main script to TradingViewHelper.py

The source is completely open, make it yours, no licenses attached.
