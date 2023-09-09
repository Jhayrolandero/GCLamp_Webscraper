import modules_to_import

class WebDriver:
    
    __private_path = r'C:\Users\OWNER\Desktop\selenium\geckodriver.exe'
    
    def _connect(self):
        firefox_option = modules_to_import.webdriver.FirefoxOptions()
        firefox_service = modules_to_import.FirefoxService(execute_path=self.__private_path)
        driver = modules_to_import.webdriver.Firefox(options=firefox_option, service=firefox_service)
        
        return driver