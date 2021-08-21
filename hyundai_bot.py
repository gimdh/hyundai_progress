import json, time, platform
from types import SimpleNamespace

from seleniumwire import webdriver



class HyundaiBot:
    def __init__(self, config):
        self.config = config


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

        if self.config.driver_path:
            filename = self.config.driver_path
        else:
            filename = self.driver_for_system()
        self.driver = webdriver.Firefox(options=options, executable_path=filename)


    def driver_for_system(self):
        machine, system = platform.machine(), platform.system()

        filename = f'./drivers/geckodriver-{system}-{machine}'
        return filename


    def login(self):
        self.driver.get(self.config.main_uri)
        time.sleep(1)
        self.driver.get(self.config.login_uri)
        time.sleep(1)
        self.wait(self.config.redirected_login_uri)

        email_element = self.driver.find_element_by_xpath(self.config.email_xpath)
        password_element = self.driver.find_element_by_xpath(self.config.password_xpath)
        button_element = self.driver.find_element_by_xpath(self.config.button_xpath)

        email_element.send_keys(self.config.email)
        password_element.send_keys(self.config.password)
        button_element.click()

        self.wait(self.config.main_uri)
        time.sleep(1)


    def query_info(self):
        self.driver.get(self.config.contract_uri)
        time.sleep(1)

        for request in self.driver.requests:
            if request.response and request.url == self.config.query_uri:
                decoded_info = request.response.body.decode('utf-8')
                return json.loads(decoded_info, object_hook=lambda d: SimpleNamespace(**d))


    def wait(self, uri):
        while(self.driver.current_url != uri):
            pass
