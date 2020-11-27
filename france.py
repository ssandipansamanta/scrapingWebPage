from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

DRIVER_PATH = 'C:\ExperimentalProject\webScraping\chromedriver\chromedriver.exe'
DESIRED_WEB_PAGE = 'https://sante.fr/recherche/trouver/DepistageCovid/Autour%20de%20moi/'

#'https://www.nintendo.com/'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get(DESIRED_WEB_PAGE)
driver.implicitly_wait(10)
mode_carte_button = driver.find_element_by_xpath(xpath='//*[@id="main"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[2]/div/ul/li[1]/button')
# //*[@id="main"]/div/div/div/div[2]/div[1]/div/div/div[3]/div[2]/button[1]/span
# print("Element is visible? " + str(mode_carte_button.is_displayed()))
driver.execute_script("$(arguments[0]).click();", mode_carte_button)

                                            # //*[@id="main"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[5]/div
# table = driver.find_element_by_xpath(xpath='//*[@id="main"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[5]/div')

all_records = pd.DataFrame(columns=['page', 'serial_no', 'name', 'address', 'phone'])
_page = 1
no_records = 1
while no_records < 3711:
    records_per_page = pd.DataFrame(columns=['page', 'serial_no', 'name', 'address', 'phone'])
    for _item in range(1, 26):
        if driver.find_element_by_xpath(xpath='//*[@id="main"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[5]/div/div['+str(_item)+']/div/div').text != '':
            name = driver.find_element_by_xpath(xpath='//*[@id="main"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[5]/div/div['+str(_item)+']/div/div[1]/div[2]/h2/a')
            address = driver.find_element_by_xpath(xpath='//*[@id="main"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[5]/div/div['+str(_item)+']/div/div[2]/div[1]/div[1]/span[1]/a[2]')
            phone = driver.find_element_by_xpath(xpath='//*[@id="main"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[5]/div/div['+str(_item)+']/div/div[2]/div[1]/div[3]')
            if 'Ferme' in phone.text or 'Fermé' in phone.text:
                phone = driver.find_element_by_xpath(xpath='//*[@id="main"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[5]/div/div['+str(_item)+']/div/div[2]/div[1]/div[4]')
        else:
            _item = _item + 1
            name = driver.find_element_by_xpath(xpath='//*[@id="main"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[5]/div/div[' + str(_item) + ']/div/div[1]/div[2]/h2/a')
            address = driver.find_element_by_xpath(xpath='//*[@id="main"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[5]/div/div[' + str(_item) + ']/div/div[2]/div[1]/div[1]/span[1]/a[2]')
            phone = driver.find_element_by_xpath(xpath='//*[@id="main"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[5]/div/div[' + str(_item) + ']/div/div[2]/div[1]/div[3]')
            if 'Ferme' in phone.text or 'Fermé' in phone.text:
                phone = driver.find_element_by_xpath(xpath='//*[@id="main"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[5]/div/div[' + str(_item) + ']/div/div[2]/div[1]/div[4]')
            _item = _item - 1
            print("png is there!!!")
        records_per_page = records_per_page.append({'page': _page, 'serial_no': _item, 'name':name.text, 'address':address.text, 'phone':phone.text}, ignore_index=True)
        records_per_page.to_csv('C:/ExperimentalProject/webScraping/output/france/output_france_page'+str(_page)+'.csv', index=False)
        all_records = all_records.append({'page': _page, 'serial_no': _item, 'name':name.text, 'address':address.text, 'phone':phone.text}, ignore_index=True)
        no_records = no_records + 1
    print("page: "+str(_page))
    if _page == 1:
        next_page = driver.find_element_by_xpath(xpath='//*[@id="main"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[6]/ul/li/a')
    else:
        next_page = driver.find_element_by_xpath(xpath='//*[@id="main"]/div/div/div/div[2]/div[1]/div/div/div[2]/div[6]/ul/li[2]/a')
    driver.execute_script("$(arguments[0]).click();", next_page)
    _page =  _page + 1
    time.sleep(10)

# required_data = table.text
driver.quit()
all_records.to_csv('C:\ExperimentalProject\webScraping\output_france_20201126.csv',index=False)
