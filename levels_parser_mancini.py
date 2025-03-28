import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import login_details
from time import sleep
import re
import json
import undetected_chromedriver as uc
from seleniumbase import Driver

def process_list_range(list_range):
    new_range = []
    for range in list_range:
        splist = range.split('-')
        low = int(splist[0])
        high = int(splist[1])
        if int(splist[1]) < 100:
            high = int(low/100)*100 + high
        if low < high:
            new_range.append([low, high])
        else:
            new_range.append([high, low])

    return new_range

def get_levels_ranges_labels(txt_in):
        #print('get_levels_ranges_labels(), txt_in=', txt_in)
        levels=[]
        labels_levels=[]
        labels_levels_lvltxt=[]
        ranges=[]
        labels_ranges=[]
        labels_ranges_lvltxt = []

        # Supports Monday are: 3690-3700, 3665, 3645, 3620, 3570-80 (major).
        if ':' in txt_in:
            splist = txt_in.split(':')[1].split('.')[0].split(',')
        else:
            splist = txt_in.split(',')

        elements = []
        for elem in splist:
            splist2 = elem.split('.')
            for val in splist2:
                elements.append(val)

        for elem in elements:
            range_temp = re.findall(r'\d+-\d+', elem)
            if len(range_temp) > 0: # this means this has ranges in it
                ranges.append(range_temp[0])
                #labels_ranges.append(str(elem).strip())
                label = re.findall("\((.*?)\)", elem)
                if len(label) > 0:
                    labels_ranges.append("(" + label[0] + ")")
                else:
                    labels_ranges.append("")
                labels_ranges_lvltxt.append(range_temp[0])
            else: # just a level
                if '(' in elem and ')' in elem:
                    sparr = elem.split('(')
                    level = int(sparr[0])
                else:
                    level = int(elem)

                levels.append(level)
                label = re.findall("\((.*?)\)", elem)
                if len(label) == 0:
                    labels_levels.append("")
                else:
                    labels_levels.append("(" + label[0] + ")")
                labels_levels_lvltxt.append(str(level))

        #print('here:', levels, labels_levels, ranges, labels_ranges)
        return levels, labels_levels, labels_levels_lvltxt, ranges, labels_ranges, labels_ranges_lvltxt


en_browser = True

options = uc.ChromeOptions()
#options.add_argument("start-maximized")
prefs = {"credentials_enable_service": False,
         "profile.password_manager_enabled": False,
         "download.prompt_for_download": False}
options.add_experimental_option("prefs", prefs)
if en_browser:
    browser = Driver(uc=True, incognito=True)
    #browser = uc.Chrome(use_subprocess=True, options=options)
    browser.maximize_window()

date_published = ""
if en_browser:
    browser.get('https://tradecompanion.substack.com/')
    browser.maximize_window()

    wait=WebDriverWait(browser, 10)

    sleep(1)
    # No thanks
    try:
        browser.find_element("xpath", ".//*[contains(text(), 'No thanks')]").click()
    except:
        pass

    #input('ready to go (y/n)? ')
    browser.find_element("xpath", ".//*[contains(text(), 'Sign in')]").click() # Sign In
    browser.find_element("xpath", ".//*[contains(text(), 'Sign in with')]").click() # Sign in with password

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[name='email']"))).send_keys(login_details.tradytics_username) #
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[name='password']"))).send_keys(login_details.tradytics_password)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[type='submit']"))).click() #continue

    # first post
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a'))).click()

    # wait till page has loaded basically
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[1]/div/div/article/div[2]/div/div[2]/div[2]/a[1]/div")))

    with open('mancini.txt', 'w', encoding="utf-8") as f:
        f.write(browser.page_source)

    # initializing tag
    res1 = re.findall("<ul>(.*?)</ul>", browser.page_source)
    idx_sr = next((idx for idx in range(len(res1)) if "supports are" in str(res1[idx]).lower()), -1)
    res2 = re.findall("<li><p>(.*?)</p></li>", res1[idx_sr])
    idx_sup = next((idx for idx in range(len(res2)) if str(res2[idx]).lower().startswith('supports')), -1)

    # "datePublished":"2022-09-14T14:01:13-07:00","dateModified":"2022-09-14T14:01:13-07:00","isAccessibleForFree"
    date_published = re.findall("\"datePublished\":\"(.*?)\",\"dateModified\"", browser.page_source)[0]
    print('date_published=', date_published)
    print('idx_sup=', idx_sup)
    txt_support = res2[idx_sup]
    txt_resistance = res2[idx_sup+2]

    print('txt_support=', txt_support)
    print('txt_resistance=', txt_resistance)
    txt_support = txt_support.replace('6k', '6000').replace('5k', '5000').replace('4k', '4000').replace('3k', '3000').replace('2k', '2000')
    txt_resistance = txt_resistance.replace('6k', '6000').replace('5k', '5000').replace('4k', '4000').replace('3k', '3000').replace('2k', '2000')

    with open('c:/temp/mancini_es_sr.txt', 'w', encoding="utf-8") as f:
        f.write(txt_support + "\n\n\n" + txt_resistance)

    os.startfile('c:/temp/mancini_es_sr.txt')

# Expected format
# Supports are: 3950, 4000, 3910-3915 (major), 3920-3925 (major).
# Resistances are: 4100, 4150, 4115-4120 (major), 4130-4135 (major).
if en_browser:
    txt_support = input('Modified txt_support: ')
    txt_resistance = input('Modified txt_resistance: ')
else:
    txt_support = "Supports are: 3910 (major; can add long if bullflagging above), 3895-3900 (can long direct; pref long touch here and reclaim ten), 3885 (major; no direct long; long if touch 3877 and pop back; shobkdn 75), 3877 (long if touch here and pop above 3885), 3840-45 (major), 3820 (major; first knilo if 3885 finally fails), 3800, 3780 (major), 3765."
    txt_resistance = "Resistances are: 3935, 3955-60 (major; one last knisho; breakout above), 3975, 4000, 4010 (major; can short), 4035 (major), 4057 (major), 4080, 4100 (major), 4110, 4118, 4127 (major)."
if en_browser:
    browser.quit()

levels_support, labels_levels_support, labels_levels_support_lvltxt, ranges_support, labels_ranges_support, labels_ranges_support_lvltxt = get_levels_ranges_labels(
    txt_support)
levels_resistance, labels_levels_resistance, labels_levels_resistance_lvltxt, ranges_resistance, labels_ranges_resistance, labels_ranges_resistance_lvltxt = get_levels_ranges_labels(
    txt_resistance)

ranges_support = process_list_range(ranges_support)
ranges_resistance = process_list_range(ranges_resistance)

print('levels_support=', levels_support)
print('ranges_support=', ranges_support)
print('levels_resistance=', levels_resistance)
print('range_resistance=', ranges_resistance)

with open('es.json', 'w') as f:
    json.dump({
    'levels_support': levels_support,
    'labels_levels_support': labels_levels_support,
    'labels_levels_support_lvltxt': labels_levels_support_lvltxt,
    'ranges_support': ranges_support,
    'labels_ranges_support': labels_ranges_support,
    'labels_ranges_support_lvltxt': labels_ranges_support_lvltxt,
    'levels_resistance': levels_resistance,
    'labels_levels_resistance': labels_levels_resistance,
    'labels_levels_resistance_lvltxt': labels_levels_resistance_lvltxt,
    'ranges_resistance': ranges_resistance,
    'labels_ranges_resistance': labels_ranges_resistance,
    'labels_ranges_resistance_lvltxt': labels_ranges_resistance_lvltxt,
    'timestamp': str(date_published)}, f, indent=2)


if en_browser:
    browser.quit()

