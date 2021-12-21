from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome, ChromeOptions

BASE_URL = "http://127.0.0.1:7000/"

class registerformtest(LiveServerTestCase):
    
    def test_connection(self):
        driver = webdriver.Chrome()
        driver.get(BASE_URL)
        assert 'Swift Vote' in driver.title
    
    def test_invalidLogin(self):
        driver = webdriver.Chrome()
        url = BASE_URL + 'login'
        driver.get(url)
        x = driver.find_element_by_name('email')
        x.send_keys('jatinsingal2@gmail.com')
        y = driver.find_element_by_name('password')
        y.send_keys('qwerty')
        driver.find_element_by_name('loginbutton').click()
        error = driver.find_element_by_id('errormsg')
        assert error.get_attribute("innerHTML") == 'Invalid Credentials'
    
    def test_register(self):
        driver = webdriver.Chrome()
        url = BASE_URL + 'register'
        driver.get(url)
        email = driver.find_element_by_name('email')  
        email.send_keys('zxcvbnm@gmail.com')
        pwd = driver.find_element_by_name('password')
        pwd.send_keys('1234')
        fname = driver.find_element_by_name('fname')
        fname.send_keys('Jatin')
        lname = driver.find_element_by_name('lname')
        lname.send_keys('Aggarwal')
        uname = driver.find_element_by_name('username')
        uname.send_keys('jsqwer')
        dob = driver.find_element_by_name('dob')
        dob.send_keys('17/04/2001')
        contact = driver.find_element_by_name('contact')
        contact.send_keys('9215840600')
        address = driver.find_element_by_name('address')
        address.send_keys('Sirsa, Haryana')
        signupButton = driver.find_element_by_name('registerbutton')
        driver.execute_script('arguments[0].click()', signupButton)
        print(driver.current_url)
        assert "http://127.0.0.1:7000/login" == driver.current_url

    def test_login(self):
        driver = webdriver.Chrome()
        url = BASE_URL + 'login'
        driver.get(url)
        email = driver.find_element_by_name('email')
        email.send_keys('jatinsingal2@gmail.com')
        pwd = driver.find_element_by_name('password')
        pwd.send_keys('1234')
        driver.find_element_by_name('loginbutton').click()
        print(driver.current_url)
        assert "http://127.0.0.1:7000/" == driver.current_url
        