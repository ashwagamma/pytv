import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import login_details
import re
import json
import undetected_chromedriver as uc
from seleniumbase import Driver

def process_list_range(list_range):
    new_range = []
    for range_cur in list_range:
        splist = range_cur.split('-')
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
    # print('get_levels_ranges_labels(), txt_in=', txt_in)
    levels = []
    labels_levels = []
    ranges = []
    labels_ranges = []

    # Supports are: 3950, 4000, 3910-3915 (major), 3920-3925 (major).
    # Resistances are: 4100, 4150, 4115-4120 (major), 4130-4135 (major).
    splist = txt_in.split(':')[1].split('.')[0].split(',')

    elements = []
    for elem in splist:
        splist2 = elem.split('.')
        for val1 in splist2:
            elements.append(val1)

    for elem in elements:
        range_temp = re.findall(r'\d+-\d+', elem)
        if len(range_temp) > 0:  # this means this has ranges in it
            ranges.append(range_temp[0])
            #labels_ranges.append(str(elem).strip())
            label = re.findall("\((.*?)\)", elem)
            if len(label) > 0:
                labels_ranges.append("("+label[0]+") "+range_temp[0])
            else:
                labels_ranges.append(range_temp[0])
        else:  # just a level
            if '(' in elem and ')' in elem:
                sparr = elem.split('(')
                level = int(sparr[0])
            else:
                level = int(elem)

            levels.append(level)
            label = re.findall("\((.*?)\)", elem)
            if len(label) == 0:
                labels_levels.append(str(level))
            else:
                labels_levels.append("(" + label[0] + ") " + str(level))

    #print('txt_in=',txt_in)
    print('here:', levels, labels_levels, ranges, labels_ranges)

    #return 0,0,0,0
    return levels, labels_levels, ranges, labels_ranges


options = uc.ChromeOptions()
#options.add_argument("start-maximized")
prefs = {"credentials_enable_service": False,
         "profile.password_manager_enabled": False}
options.add_experimental_option("prefs", prefs)
# browser = uc.Chrome(use_subprocess=True, options=options)
browser = Driver(uc=True)
browser.maximize_window()

browser.get('https://tradecompanion.substack.com/')
browser.maximize_window()

wait = WebDriverWait(browser, 10)

elem_x = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[3]/div/div/div/button"))).click()
# Sign In button top corner
browser.find_element("xpath", ".//*[contains(text(), 'Sign in')]").click()
# Sign in with password link
browser.find_element(By.XPATH, '/html/body/div/div/div[2]/div[2]/form/div[2]/div/a').click()
#username
wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div[2]/form/div[1]/input"))).send_keys(login_details.substack_username)
#password
wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div[2]/form/input[3]"))).send_keys(login_details.substack_password)
#sign in button
wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div[2]/form/button'))).click()

# first post
wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a"))).click()

# wait till page has loaded
wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[1]/div/article/div[4]/div[1]")))

#flag=input('y/n:')

with open('mancini.txt', 'w', encoding="utf-8") as f:
    f.write(browser.page_source)

txt = browser.page_source
txt = txt.replace('<span>', '')
txt = txt.replace('</span>', '')
txt = txt.replace('<strong>', '')
txt = txt.replace('</strong>', '')
txt = txt.replace('<em>', '')
txt = txt.replace('</em>', '')
# initializing tag
tag = "p"
# regex to extract required strings
reg_str = "<" + tag + ">(.*?)</" + tag + ">"
res = re.findall(reg_str, txt)

txt2 = browser.page_source
reg_str = "<li><p>(.*?)</p></li>"
res2 = re.findall(reg_str, txt)
idx_sup = 0
for idx in range(0,len(res2)):
    val = res2[idx]
    if str(val).lower().startswith('supports'):
        idx_sup = idx
    print(idx, val)
    #print('res2 val=', val)

#"datePublished":"2022-09-14T14:01:13-07:00","dateModified":"2022-09-14T14:01:13-07:00","isAccessibleForFree"
date_published = re.findall("\"datePublished\":\"(.*?)\",\"dateModified\"", txt)[0]
print('date_published=', date_published)

txt_support = res2[idx_sup]
txt_resistance = res2[idx_sup+2]

txt_support = txt_support.replace('4k', '4000')
txt_support = txt_support.replace('3k', '3000')
txt_support = txt_support.replace('2k', '2000')

txt_resistance = txt_resistance.replace('4k', '4000')
txt_resistance = txt_resistance.replace('3k', '3000')
txt_resistance = txt_resistance.replace('2k', '2000')

with open('c:/temp/mancini_es_sr.txt', 'w', encoding="utf-8") as f:
    f.write(txt_support+"\n\n\n"+txt_resistance)

os.startfile('c:/temp/mancini_es_sr.txt')

# Expected format
# Supports are: 3950, 4000, 3910-3915 (major), 3920-3925 (major).
# Resistances are: 4100, 4150, 4115-4120 (major), 4130-4135 (major).
txt_support = input('Modified txt_support: ')
txt_resistance = input('Modified txt_resistance: ')
browser.quit()

levels_support, labels_levels_support, ranges_support, labels_ranges_support = get_levels_ranges_labels(txt_support)
levels_resistance, labels_levels_resistance, ranges_resistance, labels_ranges_resistance = get_levels_ranges_labels(txt_resistance)

ranges_support = process_list_range(ranges_support)
ranges_resistance = process_list_range(ranges_resistance)

print('levels_support=', levels_support)
print('new ranges_support=', ranges_support)
print('levels_resistance=', levels_resistance)
print('new range_resistance=', ranges_resistance)

#with open('readme.txt', 'w', encoding="utf-8") as f:
#    for val in res:
#        f.write(str(val))
#        f.write('\n\n')

with open('es.json', 'w') as f:
    json.dump({
        'levels_support': levels_support,
        'ranges_support': ranges_support,
        'levels_resistance': levels_resistance,
        'ranges_resistance': ranges_resistance,
        'labels_levels_support': labels_levels_support,
        'labels_ranges_support': labels_ranges_support,
        'labels_levels_resistance': labels_levels_resistance,
        'labels_ranges_resistance': labels_ranges_resistance,
        'timestamp': str(date_published)}, f, indent=2)

browser.quit()
