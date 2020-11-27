from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait

DRIVER_PATH = 'C:\ExperimentalProject\webScraping\chromedriver\chromedriver.exe'
DESIRED_WEB_PAGE = 'https://www.arcgis.com/home/item.html?id=11fe8f374c344549815a716c8472832f&view=list&sortOrder=desc&sortField=defaultFSOrder#data/'
#'https://www.nintendo.com/'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get(DESIRED_WEB_PAGE)

header = ['Facility ID', 'Name of Facility',	'Full Address',	'Municipality',	'Owner Name',	'Owner Type',	'Phone',	'Website',	'Operational Hours',	'Comments',	'Instructions',	'Vehicle Capacity',	'Daily Testing Capacity',	'Status',	'CreationDate',	'EditDate',	'Vetted',	'Drive-through',	'Appointment Only',	'Referral Required',	'Services Offered',	'Call first',	'Virtual/Telehealth Screening',	'Local Health Department URL',	'State or Territory',	'Data Source',	'County',	'Red Flag?',	'Volunteer Note',	'Public Form Submission',	'Testing Start Date',	'Testing End Date',	'Kind of test',	'Processing location',	'Fine Print (requires study participation, no insurance accepted, etc.)',	'Vehicle Required',	'Facility Type',	'Outside Feature ID',	'Filter',	'Minimum Age',	'Offering same-day diagnostic (not antibody) results',	'Offering Take-Home Test','Objective ID']
field_no = [1,	2,	3,	4,	5,	6,	7,	8,	9,	10,	11,	12,	13,	14,	15,	16,	17,	18,	19,	20,	21,	22,	23,	24,	25,	27,	28,	29,	30,	31,	32,	33,	34,	35,	36,	37,	38,	39,	40,	41,	42,	43,	44]
# _r = 1
_c = 1
_row_number = 1
while _row_number < 100:
    # elements = driver.find_elements_by_xpath("//div[contains(@id, 'dgrid_0-row-')]")
    # time.sleep(10)
    elements = driver.find_elements_by_xpath("//*[contains(@id, 'dgrid_0-row-')]")
    ids_df = pd.DataFrame(columns=['row'])
    for _id in range(0, len(elements)):
        ids_df = ids_df.append({'row': float(elements[_id].get_attribute('id')[12:])}, ignore_index=True)
    max_id = max(ids_df['row'])
    if _c == 1:
        min_id = min(ids_df['row'])

    if min_id < max_id:
        _c = _c + 1
        print("Number of visible rows:" + str(len(elements)))
        for _r in range(2,(len(elements)+1)):
            records_per_row = pd.DataFrame(columns=[header])
            records = []
            for _f in field_no:
                obj = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/div/div[2]/main/div[3]/div[2]/div[2]/div/div[1]/div/div/div[2]/div/div[2]/div/div['+str(_r)+']/table/tr/td['+str(_f)+']')))
                driver.execute_script("return arguments[0].scrollIntoView();", obj)
                # driver.execute_script("return arguments[0].scrollTo(0, document.body.scrollHeight);", obj)
                row = driver.find_element_by_xpath(xpath='/html/body/div[2]/div/div[2]/div/div[2]/main/div[3]/div[2]/div[2]/div/div[1]/div/div/div[2]/div/div[2]/div/div['+str(_r)+']/table/tr/td['+str(_f)+']')
                if row.is_displayed():
                    record = row.text
                else:
                    record = driver.execute_script("return arguments[0].textContent", row)

                records = records + [record]

            dictionary = dict(zip(header, records))
            records_per_row = pd.DataFrame(dictionary, index=[0])
            records_per_row['row_number'] = _row_number
            records_per_row.to_csv('C:/ExperimentalProject/webScraping/output/us/output_us_row_' + str(_row_number) + '.csv', index=False)
            # time.sleep(2)
            print("# Row: " + str(_row_number) + " Current Time: " + time.strftime("%H:%M:%S", time.localtime()))
            _row_number = _row_number + 1
            min_id = max_id
        # _c = _c + len(elements)


driver.quit()
# '/html/body/div[2]/div/div[2]/div/div[2]/main/div[3]/div[2]/div[2]/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/table/tr/td[2]/div'
# '/html/body/div[2]/div/div[2]/div/div[2]/main/div[3]/div[2]/div[2]/div/div[1]/div/div/div[2]/div/div[2]/div/div[3]/table/tr/td[2]/div'
# '/html/body/div[2]/div/div[2]/div/div[2]/main/div[3]/div[2]/div[2]/div/div[1]/div/div/div[2]/div/div[2]/div/div[30]/table/tr/td[2]/div'
# '/html/body/div[2]/div/div[2]/div/div[2]/main/div[3]/div[2]/div[2]/div/div[1]/div/div/div[2]/div/div[2]/div/div[29]/table/tr/td[2]/div'
