from WebDriver import WebDriver
import modules_to_import

class LoginCtrl(WebDriver):
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url
        self.driver = super()._connect()
        
    # Wait for input to appear
    def __wait_login_input(self):
        try:
            self.driver.find_element('id', 'param1').send_keys(self.username)
            self.driver.find_element('id', 'param2').send_keys(self.password)
            self.driver.find_element('id', 'param2').send_keys(modules_to_import.Keys.ENTER)        
            return True
        except:
            raise print("Some error")
    
    # Wait for web response
    def __handle_login(self):
        self.driver.get(self.url)
        wait = modules_to_import.WebDriverWait(self.driver, timeout=10).until(lambda driver: driver.find_element('class name', 'text-center'))
        
        if wait: return True
        else: return False
    
    # Login the user
    def login_user(self):   
        if(self.__handle_login()):
            if(self.__wait_login_input()):
                return True
            else:return False
        else:return False
        
    def return_driver(self):
        return self.driver