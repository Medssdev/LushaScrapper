import json
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import requests
from requests.cookies import cookiejar_from_dict

base = os.path.dirname(os.path.abspath(__file__))


class LushaSession:
    CONTACTS_URL = 'https://dashboard-services.lusha.com/v2/prospecting-full'

    def __init__(self):
        self.cookies = self.load_saved_cookies()
        self.session = requests.session()
        self.session.cookies = cookiejar_from_dict(self.cookies)
        self.session.headers.update(self.headers())

    @classmethod
    def load_saved_cookies(cls):
        cookie_path = os.path.join(base, 'session', 'cookie.json')
        if os.path.exists(cookie_path):
            with open(cookie_path) as f:
                return json.load(f)
        else:
            return cls.extract_cookies()

    @classmethod
    def extract_cookies(cls):
        driver = webdriver.Chrome(os.path.join(base, 'driver', 'chromedriver.exe'))
        wait = WebDriverWait(driver, 100)
        cookies = {}

        driver.get('https://auth.lusha.com/login')
        wait.until(lambda dr: str(dr.current_url).endswith('dashboard'))

        for c in driver.get_cookies():
            cookies[c.get('name')] = c.get('value')

        with open(os.path.join(base, 'session', 'cookie.json'), 'w') as f:
            json.dump(cookies, f)

        driver.close()

        return cookies

    def headers(self):
        return {
            'Origin': 'https://dashboard.lusha.com',
            '_csrf': self.cookies['_csrf'],
            "X-XSRF-TOKEN": self.cookies['XSRF-TOKEN']
        }

    def get_contacts(self, contact_filter: dict):
        response = self.session.post(url=self.CONTACTS_URL, json=contact_filter)
        if response.status_code == 401:
            print('Session Expired ! Log in...')
            self.session.cookies = cookiejar_from_dict(self.extract_cookies())
            return self.get_contacts(contact_filter)
        return response

