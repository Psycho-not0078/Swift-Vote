from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from selenium.webdriver import Chrome, ChromeOptions
import time
BASE_URL = "http://127.0.0.1:8000/"
class registerformtest(LiveServerTestCase):
    
    def test_connection(self):
        driver = webdriver.Chrome()
        driver.get(BASE_URL)
        assert 'Swift Vote' in driver.title
    
    def test_invalidLogin(self):
        driver = webdriver.Chrome()
        url = BASE_URL + 'login'
        driver.get(url)
        x = driver.find_element_by_name('email')  # Find the search box
        x.send_keys('jatinsingal2@gmail.com')
        y = driver.find_element_by_name('password')
        y.send_keys('qwerty')
        driver.find_element_by_name('loginbutton').click()
        error = driver.find_element_by_id('errormsg')
        assert error.get_attribute("innerHTML") == 'Invalid Credentials'
    
    def test_login(self):
        driver = webdriver.Chrome()
        url = BASE_URL + 'login'
        driver.get(url)
        email = driver.find_element_by_name('email')  # Find the search box
        email.send_keys('jatinsingal2@gmail.com')
        pwd = driver.find_element_by_name('password')
        pwd.send_keys('1234')
        driver.find_element_by_name('loginbutton').click()
        
        time.sleep(3)

        username = driver.find_element_by_id('loginusername')
        assert username.get_attribute("innerHTML") == 'Hi, Jatin Singal'
    
    def test_logout(self):
        driver = webdriver.Chrome()
        driver.get(BASE_URL)
        logoutButton = driver.find_element_by_id('logout')
        driver.execute_script('arguments[0].click()', logoutButton)
        username = driver.find_element_by_id('loginusername')
        assert username.get_attribute("innerHTML") == ''

    def test_register(self):
        driver = webdriver.Chrome()
        url = BASE_URL + 'register'
        driver.get(url)
        email = driver.find_element_by_name('email')  # Find the search box
        email.send_keys('jatinsi@gmail.com')
        pwd = driver.find_element_by_name('password')
        pwd.send_keys('1234')
        fname = driver.find_element_by_name('fname')
        fname.send_keys('Jatin')
        lname = driver.find_element_by_name('lname')
        lname.send_keys('Aggarwal')
        uname = driver.find_element_by_name('username')
        uname.send_keys('ja')
        dob = driver.find_element_by_name('dob')
        dob.send_keys('17/04/2001')
        contact = driver.find_element_by_name('contact')
        contact.send_keys('9215840600')
        address = driver.find_element_by_name('address')
        address.send_keys('Sirsa, Haryana')
        signupButton = driver.find_element_by_name('registerbutton')
        driver.execute_script('arguments[0].click()', signupButton)
        
        time.sleep(3)

        email = driver.find_element_by_name('email')  # Find the search box
        email.send_keys('jatinsi@gmail.com')
        pwd = driver.find_element_by_name('password')
        pwd.send_keys('1234')
        driver.find_element_by_name('loginbutton').click()
        
        time.sleep(3)

        username = driver.find_element_by_id('loginusername')
        assert username.get_attribute("innerHTML") == 'Hi, Jatin Aggarwal'
    # def testregister(self):
    #     driver = webdriver.Chrome()
    #     driver.get('http://127.0.0.1:8000/register')
    #     assert "Sign Up" in driver.title



# EMAIL_ID = "jatinsingal2@gmail.com"
# EXPECTED_COLOR = "rgba(222, 20, 33, 1)"


# class BrowserstackCrawler(object):
#    def __init__(self):
#       # Visit chrome://version/ and copy profile path in place of '<chrome user profile>'
#       options = ChromeOptions().add_argument("--user-data-dir=<chrome user profile>")
#       self.browser = Chrome(chrome_options=options)
#       self.browser.get(BASE_URL)

#    def signup(self):
#     #   cookie_cta = self.browser.find_element_by_id('accept-cookie-notification')
#     #   cookie_cta.click()

#       # Navigate to Signup Page
#       button = self.browser.find_element_by_id('register')
#       button.click()

#       time.sleep(2)

#       # Fill user's full name
#       username = self.browser.find_element_by_id('user_full_name')
#       # username.send_keys('John Doe')
#       self.slow_typing(username, 'John Doe')

#       time.sleep(1)
#       # Fill user's email ID
#       email = self.browser.find_element_by_id('user_email_login')
#       self.slow_typing(email, EMAIL_ID)

#       time.sleep(2)
#       # Fill user's password
#       password = self.browser.find_element_by_id('user_password')

#       # Reads password from a text file because
#       # it's silly to save the password in a script.
#       with open('password.txt', 'r') as myfile:
#          Password = myfile.read().replace('\n', '')
#       self.slow_typing(password, Password)

#       time.sleep(1)
#       # click on Terms and Condition
#       toc = self.browser.find_element_by_name('terms_and_conditions')
#       toc.click()

#       # click on signup page
#       signupbutton = self.browser.find_element_by_id('user_submit')
#       signupbutton.click()

#       # increase time so that you can manually pass Recaptcha
#       # verification and confirm your email
#       time.sleep(20)

#       self.close_browser()

#    def validate_signupform(self):
#        cookie_cta = self.browser.find_element_by_id('accept-cookie-notification')
#        cookie_cta.click()
#        # Navigate to Signup Page
#        button = self.browser.find_element_by_id('signupModalButton')
#        button.click()

#        time.sleep(4)

#        # click on signup page
#        signupbutton = self.browser.find_element_by_id('user_submit')
#        signupbutton.click()


#        username = self.browser.find_element_by_id('user_full_name')
#        if "error" in username.get_attribute('outerHTML'):
#           obtained_color = username.value_of_css_property('border-bottom-color')
#           if not self.check_color(obtained_color, "rgba(222, 20, 33, 1)"):
#              print(f"expected color is {EXPECTED_COLOR} and got {obtained_color}")

#        email = self.browser.find_element_by_id('user_email_login')
#        if "error" in email.get_attribute('outerHTML'):
#           obtained_color = email.value_of_css_property('border-bottom-color')
#           if not self.check_color(obtained_color, "rgba(222, 20, 33, 1)"):
#              print(f"expected color is {EXPECTED_COLOR} and got {obtained_color}")

#        password = self.browser.find_element_by_id('user_password')
#        if "error" in password.get_attribute('outerHTML'):
#           obtained_color = password.value_of_css_property('border-bottom-color')
#           if not self.check_color(obtained_color, "rgba(222, 20, 33, 1)"):
#              print(f"expected color is {EXPECTED_COLOR} and got {obtained_color}")

#        error_messages = ["At least 3 characters",
#                            "Invalid Email", "At least 6 characters"]
#        message_body_html_elements = self.browser.find_elements_by_class_name('msg-body')
#        for msg in message_body_html_elements:
#           error_msg = msg.get_attribute('innerHTML').split("span")[1][1:-2]
#           if error_msg not in error_messages:
#              print(f"{msg.get_attribute('outerHTML')} is missing error message")

#        self.close_browser()


#    def slow_typing(self, element, text):
#       for character in text:
#          element.send_keys(character)
#          time.sleep(0.3)


#    def check_color(self, color, orginal_color):
#       return color == orginal_color

#    def close_browser(self):
#       self.browser.close()


# b1 = BrowserstackCrawler()
# b1.signup()
# b2 = BrowserstackCrawler()
# b2.validate_signupform()