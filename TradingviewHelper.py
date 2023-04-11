import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import login_details
from time import sleep
import undetected_chromedriver as uc


class TradingviewHelper(object):

    def __init__(self, download_dir=None):
        self.browser = self.login(download_dir)  # expected format: "c:\\temp\\charts\\"
        self.wait = WebDriverWait(self.browser, 10)
        self.action_chains = ActionChains(self.browser)

    @staticmethod
    def login(download_dir):
        options = uc.ChromeOptions()
        options.add_argument("start-maximized")
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        browser = uc.Chrome(use_subprocess=True, options=options)
        browser.maximize_window()

        #with open('readme.txt', 'w', encoding="utf-8") as f:
        #    f.write(browser.page_source)

        browser.get("https://www.tradingview.com/#signin")
        wait = WebDriverWait(browser, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Email']"))).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[name='username']"))).send_keys(
            login_details.tradingview_username)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[name='password']"))).send_keys(
            login_details.tradingview_password)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(., 'Sign in')]]"))).click()
        sleep(2)

        return browser

    def delete_all_lines_and_price_ranges(self):
        sleep(2)
        wait = WebDriverWait(self.browser, 10)
        #flag=input('continue?')
        # Toggle the base/alerts to make sure it's enabled, then scroll down to object tree and click on it
        elem_base = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-name='base']")))
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-name='alerts']"))).click()
        self.action_chains.move_to_element(elem_base).click().perform()
        self.action_chains.send_keys(Keys.PAGE_DOWN).perform()
        elem_object_tree = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-name='object_tree']")))
        self.action_chains.move_to_element(elem_object_tree).click().perform()

        #flag = input('press to continue...')
        # Use below code to delete all horizontal lines and price ranges, loop over all drawings
        x = 2
        while x < 100:
            try:
                elem_tree = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "tree-MgF6KBas")))
                elem_tree.find_element(By.XPATH, './/div[2]/div/div[' + str(x) + ']')  # This line is used to bail the try-except with an exception if no more drawings are present
                try:
                    elem_title = elem_tree.find_element(By.XPATH, './/div[2]/div/div[' + str(x) + ']/div/span/span[2]')
                    ttl = elem_title.text
                except:  # we allow exception to pass because this is just a separator element with no title field
                    ttl = 'separator'
                    pass
                #print('x=', x, ', ttl=', ttl)
                if any(y in str(ttl).lower() for y in ['horizontal line', 'price range', 'horizontal ray', 'trend line', 'vwap']):
                    #print('here??')
                    elem_x = elem_tree.find_element(By.XPATH, './/div[2]/div/div[' + str(x) + ']/div/span/span[3]/span[3]')
                    self.action_chains.move_to_element(elem_x).click().perform()
                else:
                    x = x + 1
            except:
                break

    def draw_horizontal_line(self, level, template, label=None):
        print('TradingViewHelper().draw_horizontal_line().level,template =', str(level), str(template))
        wait = WebDriverWait(self.browser, 10)
        # Need this step to bring up the lines popup menu
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-name='linetool-group-trend-line']")))
        self.action_chains.move_to_element(element).double_click().perform()

        # In the menu click on horizontal line
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-name='LineToolHorzLine']")))
        self.action_chains.move_to_element(element).click().perform()

        val = random.randint(1, 12)
        val2 = random.randint(13, 25)
        # click in the canvas so the line is drawn, needed for first line
        elem_canvas_main = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "chart-markup-table")))
        elem_canvas = elem_canvas_main.find_element(By.XPATH, './/tr[3]/td[2]/div')
        self.action_chains.move_to_element_with_offset(elem_canvas, val, val2).click().perform()
        #sleep(2)
        # Click on settings icon
        elem_drawing_toolbar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-name='drawing-toolbar']")))
        elem_settings = elem_drawing_toolbar.find_element(By.CSS_SELECTOR, "[data-name='settings']")
        self.action_chains.move_to_element(elem_settings).click().perform()

        #sleep(1)
        # Styles
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-id='source-properties-editor-tabs-style']"))).click()
        # Select template
        elem_footer = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "footer-PhMf7PhQ")))
        elem_footer.find_element(By.XPATH, './/span').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='"+template+"']"))).click()

        # Coordinates
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-id='source-properties-editor-tabs-coordinates']"))).click()
        #sleep(1)
        self.action_chains.send_keys(level).send_keys(Keys.TAB).perform()

        # Text
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-id='source-properties-editor-tabs-text']"))).click()
        #sleep(1)
        self.action_chains.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL).perform()
        self.action_chains.send_keys(str(label)).perform()

        # Click on Ok
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-name='submit-button']"))).click()
        #sleep(1)

    def draw_price_range(self, level_low, level_high, template):
        print('TradingViewHelper().draw_price_range().level_low,level_high,template =', str(level_low), str(level_high), template)
        # Need this step to bring up the price range popup menu
        wait = WebDriverWait(self.browser, 10)

        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-name='linetool-group-prediction-and-measurement']")))
        self.action_chains.move_to_element(element).double_click().perform()

        # In the menu click on Price range
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-name='LineToolPriceRange']"))).click()

        # click in the canvas twice so the range is drawn
        elem_canvas_main = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "chart-markup-table")))
        elem_canvas = elem_canvas_main.find_element(By.XPATH, './/tr[3]/td[2]/div')

        val = random.randint(1, 120)
        val2 = random.randint(130, 250)

        self.action_chains.move_by_offset(val, val).click(elem_canvas).perform()
        self.action_chains.move_by_offset(val2, val2).click(elem_canvas).perform()

        #sleep(1)

        # Click on settings icon
        elem_drawing_toolbar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-name='drawing-toolbar']")))
        elem_settings = elem_drawing_toolbar.find_element(By.CSS_SELECTOR, "[data-name='settings']")
        self.action_chains.move_to_element(elem_settings).click().perform()

        # Select template
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-id='source-properties-editor-tabs-style']"))).click()
        elem_footer = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "footer-PhMf7PhQ")))
        elem_footer.find_element(By.XPATH, './/span').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='"+template+"']"))).click()

        #sleep(2)
        # Coordinates
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-id='source-properties-editor-tabs-coordinates']"))).click()
        #sleep(2)
        self.action_chains.send_keys(level_low).send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(level_high)
        self.action_chains.perform()

        #sleep(1)
        # Click Ok in styles
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-name='submit-button']"))).click()

    def change_symbol(self, symbol):
        self.action_chains.send_keys(symbol).send_keys(Keys.ENTER).perform()

    def save_chart_to_file(self):
        self.action_chains.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('s').key_up(Keys.ALT).key_up(Keys.CONTROL).perform()

    def open_chart(self, url_chart):
        self.browser.get(url_chart)
        sleep(2)

    def save_chart(self):
        self.action_chains.key_down(Keys.CONTROL).send_keys('s').perform()
        sleep(3)
        self.action_chains.key_up(Keys.CONTROL).perform()

    def quit(self):
        self.browser.quit()
