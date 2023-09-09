from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
from flask import jsonify

class Todo_List:
    
    def get_driver(self, driver):
        self.driver = driver
        
    def make_json(self):
        data = self.get_activities()
        self.driver.close()
        return jsonify(data)
        
    def make_csv(self):
        data = self.get_activities()
        
        df = pd.DataFrame(data)
        csv_filename = "Activities.csv"
        df.to_csv(csv_filename, index=False)
        print("File is completed")
        self.driver.close()
        
    def __get_page_source(self):
        page_source = self.driver.page_source
        return BeautifulSoup(page_source, 'html.parser')
        
    def __go_to_todolist(self):
        WebDriverWait(self.driver, timeout=100).until(lambda driver: driver.find_element('class name', 'class__header'))
        self.driver.get("https://gordoncollegeccs.edu.ph/ccs/students/lamp/#/main/todolist")
        WebDriverWait(self.driver, timeout=100).until(lambda driver: driver.find_element('class name', 'panel-list'))
        
    def get_activities(self):
        self.__go_to_todolist()
        soup = self.__get_page_source()
        parents = soup.find_all('section', class_="ng-star-inserted")
        
        data = {
            "Subject": [],
            "Activity": [],
            "Submission": []
        }
        for parent in parents:
            activity = parent.find_all("div", class_="panel-list")
            for act in activity:
                title = parent.find("div", class_="taskheader")
                # print(title.text)
                act_info = act.find("div", class_="activityheader__info")
                act_title = act_info.find("h6")
                # print(act_title.text)
                date_sub = act_info.find("p").text
                date_sub = date_sub.lstrip("Due Date:")
                # print(date_sub.text)
                data["Subject"].append(title.text)
                data["Activity"].append(act_title.text)
                data["Submission"].append(date_sub)

        return data