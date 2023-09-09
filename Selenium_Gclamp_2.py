"""
Procedural scraping 
Not working properly
"""

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import os
from win10toast import ToastNotifier

toaster = ToastNotifier()
USERNAME = 'Your username here'
PASSWORD = 'Add your password here'
GECKODRIVER_PATH = r'Change the file location of your geckodriver'
firefox_options = webdriver.FirefoxOptions()
firefox_service = FirefoxService(executable_path=GECKODRIVER_PATH)
driver = webdriver.Firefox(options=firefox_options, service=firefox_service)

class CustomError(Exception):
    pass

def get_page_source():
    page_source = driver.page_source
    return BeautifulSoup(page_source, 'html.parser')

def website_to_scrape(starting_url):
    try:
        driver.get(url=f'{starting_url}')
        
        wait = WebDriverWait(driver, timeout=10).until(lambda driver: driver.find_element('class name', 'text-center'))
        if wait.text:    
            driver.find_element('id', 'param1').send_keys(USERNAME)
            driver.find_element('id', 'param2').send_keys(PASSWORD)
            driver.find_element('id', 'param2').send_keys(Keys.ENTER)        
            
            return True
        
        else:
            print('Error, try again')
            
            return False
    except:
        print("Something is wrong, try again later")
        driver.quit()

        return False
        
        
def get_activities_and_date():
    
    try:
        wait = WebDriverWait(driver, timeout=100).until(lambda driver: driver.find_element('class name', 'class__card'))    
        if not wait.text:
            raise CustomError('Some Error')
        
        driver.find_element('class name', 'class__enter').click()
        
        wait = WebDriverWait(driver, timeout=100).until(lambda driver: driver.find_element('class name', 'materials'))
        if not wait.text:
            raise CustomError('Some Error')

        soup = get_page_source()
        
        parent_header = soup.find('header')
        
        subject_title = parent_header.find('h2')        
        activities = soup.select('[style="color: var(--clr-neutral);"]')
        date = soup.select('[style="margin-top: .5em;"]')
        
        activity_date = zip(activities, date)
        
        scrapped_data = {}
        
        scrapped_data['Subject'] = subject_title
        scrapped_data['Activity'] = []
        scrapped_data['Deadline'] = []
        
        for activity, date in activity_date:
            scrapped_data['Activity'].append(activity.text)
            scrapped_data['Deadline'].append(date.text)

        return scrapped_data

    except:
        print("Something's wrong, try again later!")
        driver.quit()
        return False
    
def make_excel_file(scrapped_data):
    
    df = pd.DataFrame(scrapped_data)
    file_path = 'output.xlsx'
    
    if os.path.exists(file_path):
        os.remove(file_path)
        
    df.to_excel(file_path, index=False)
    toaster.show_toast("Script Notification", "Scrapping is done!", duration=10)
    
    os.startfile(file_path)
    
    driver.quit()
    
        
response = website_to_scrape('https://gordoncollegeccs.edu.ph/ccs/students/lamp/#/login')

if response:
    scrapped_data = get_activities_and_date()
    
    if scrapped_data:
        make_excel_file(scrapped_data)
    else:
        os.startfile('Selenium_Gclamp_2.py')

else:
    os.startfile('Selenium_Gclamp_2.py')
    
