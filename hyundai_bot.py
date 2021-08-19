import json, time
from types import SimpleNamespace

from seleniumwire import webdriver



class HyundaiBot:
    def __init__(self, config_file='config.json'):
        with open(config_file) as f:
            self.config = json.load(f, object_hook=lambda d: SimpleNamespace(**d))


    def get_info(self):
        self.create_driver()
        self.login()
        info = self.query_info()

        self.driver.quit()
        del self.driver
        return info


    def create_driver(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options, executable_path=self.config.driver_path)


    def login(self):
        self.driver.get(self.config.login_uri)
        self.wait(self.config.redirected_login_uri)

        email_element = self.driver.find_element_by_xpath(self.config.email_xpath)
        password_element = self.driver.find_element_by_xpath(self.config.password_xpath)
        button_element = self.driver.find_element_by_xpath(self.config.button_xpath)

        email_element.send_keys(self.config.email)
        password_element.send_keys(self.config.password)
        button_element.click()

        self.wait(self.config.login_complete_uri)


    def query_info(self):
        self.driver.get(self.config.contract_uri)
        time.sleep(3)

        for request in self.driver.requests:
            if request.response and request.url == self.config.query_uri:
                decoded_info = request.response.body.decode('utf-8')
                return json.loads(decoded_info, object_hook=lambda d: SimpleNamespace(**d))


    def wait(self, uri):
        while(self.driver.current_url != uri):
            pass
