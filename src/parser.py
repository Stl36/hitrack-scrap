from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from payload import login, password


class HitrackParser:
    def __init__(self, url, login, password):
        self.url = url
        self.login = login
        self.password = password
        self.driver = self.setup_driver()

    def setup_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        return webdriver.Chrome(options=options)

    def login_to_site(self):
        self.driver.get(self.url)
        dropdown = self.driver.find_element(By.NAME, "ListId")
        select = Select(dropdown)
        select.select_by_value(self.login)
        password_field = self.driver.find_element(By.NAME, value="pword")
        password_field.send_keys(self.password)
        password_field.submit()

    def switch_to_frame(self, frame_name):
        try:
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(ec.presence_of_element_located((By.XPATH, f"//frame[@name='{frame_name}']")))
            frame = self.driver.find_element(By.XPATH, f"//frame[@name='{frame_name}']")
            self.driver.switch_to.frame(frame)
        except Exception as e:
            print(f"Не удалось найти {frame_name} \n {e}")

    def click_summary_button(self):
        try:
            self.switch_to_frame('headFrame')
            summary_button = self.driver.find_element(By.XPATH, "//input[@name='summary']")
            summary_button.click()
            self.driver.switch_to.default_content()
        except Exception as e:
            print(f"Не удалось найти кнопку Summary {e}")
            print(self.driver.page_source)

    def get_table_data(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(ec.presence_of_element_located((By.XPATH, "/html/body/form/p[3]/table/tbody")))
            row_table0 = self.driver.find_elements(By.XPATH, "/html/body/form/p[3]/table/tbody//tr/td")
            """получчаем список в котором лежат события  """
            return row_table0
        except Exception as e:
            print(f"Не удалось найти таблицы\n{e}")
            return None, None

    def parse_table_data(self, table_data):
        list_of_keys = ('Item', 'Name', 'Location', 'Group', 'Type', 'Model', 'Serial', 'Status', 'Last Communication',
                        'Site ID', 'IP Address 1', 'IP Address 2')
        active_triggers = []
        if len(table_data) > 11:
            counts = len(table_data)/12
            counts = int(counts)
            for count in range(counts):
                nested_dict = {}
                modifyer = count*12
                for el in range(len(list_of_keys)):
                    nested_dict[list_of_keys[el]] = table_data[el+modifyer].text
                active_triggers.append(nested_dict)
        return active_triggers

    def run(self):
        dynamic_list = []
        self.login_to_site()
        self.click_summary_button()
        self.switch_to_frame('bodyFrame')
        table_data = self.get_table_data()
        if table_data[0] or table_data[1]:
            dynamic_list = self.parse_table_data(table_data)
        self.driver.quit()
        return dynamic_list


url = 'http://192.168.226.21/CGI-LOGON'
parser = HitrackParser(url, login, password)
