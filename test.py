import pytest
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://b2c.passport.rt.ru/account_b2c/page'
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(10)

class element_has_css_class(object):
    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if self.css_class in element.get_attribute("class"):
            return element
        else:
            return False

@pytest.fixture(autouse=True)
def driver():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    pytest.driver = webdriver.Chrome(service=service)
    pytest.driver.maximize_window()
    pytest.driver.get(url)
    yield
    pytest.driver.quit()

def test_first():
    pytest.driver = webdriver.Chrome('/Users/apple/Downloads/chromedriver.exe')
    pytest.driver.get(url)
    yield
    pytest.driver.quit()

def test_successful_tab():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-phone')))
    assert pytest.driver.find_element(By.ID, 't-btn-tab-phone').text != 'Номер'
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    assert pytest.driver.find_element(By.ID, 't-btn-tab-mail').text == 'Почта'
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-login')))
    assert pytest.driver.find_element(By.ID, 't-btn-tab-login').text == 'Логин'
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-ls')))
    assert pytest.driver.find_element(By.ID, 't-btn-tab-ls').text == 'Лицевой счёт'

#Телефон
def test_successful_authorization_by_phone():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('89164112944')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('12qw!@QW')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.CLASS_NAME, 'user-name__first-patronymic').text == "Маргарита"

def test_unsuccessful_unregistered_number():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('89154112944')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('12qw!@QW')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

def test_incorrect_password_by_phone():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('89164112944')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('111111111')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

def test_successful_authorization_by_phone_without_code():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('9164112944')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('12qw!@QW')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.CLASS_NAME, 'user-name__first-patronymic').text == "Маргарита"

def test_unsuccessful_entering_letters_by_phone():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('rtyuiolrtyu')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('12qw!@QW')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

#Почта
def test_successful_authorization_by_email():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('mspromargo@gmail.com')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('12qw!@QW')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.CLASS_NAME, 'user-name__first-patronymic').text == "Маргарита"

def test_unsuccessful_authorization_by_invalid_email():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('promargo@gmail.com')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('12qw!@QW')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

def test_unsuccessful_by_incorrect_email_without_code():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('mspromargo@gmail')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('12qw!@QW')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

def test_unsuccessful_by_incorrect_email_without_server_address():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('mspromargo.com')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('12qw!@QW')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

def test_incorrect_password_by_email():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('mspromargo@gmail.com')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('11111111')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

#Лицевой счет
def test_successful_authorization_by_login():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 't-btn-tab-login').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('rtkid_1697549778905')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('12qw!@QW')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.CLASS_NAME, 'user-name__first-patronymic').text == "Маргарита"

def test_unsuccessful_authorization_by_invalid_login():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 't-btn-tab-login').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('rrtkid_1697549778905')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('12qw!@QW')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

def test_incorrect_password_by_login():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 't-btn-tab-login').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('rtkid_1697549778905')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('11111111')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

def test_successful_authorization_by_invalid_ls():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-ls')))
    pytest.driver.find_element(By.ID, 't-btn-tab-ls').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('069754977890')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('1111111111')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

def test_incorrect_password_by_ls():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-ls')))
    pytest.driver.find_element(By.ID, 't-btn-tab-ls').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('1697549778905')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('1111111111')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

#по временному коду
def test_authorization_by_code_with_phone():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('89164112944')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('12qw!@QW')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'lk-btn')))
    pytest.driver.find_element(By.ID, 'lk-btn').click()
    element = WebDriverWait(pytest.driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, 'iqOiiv')))
    pytest.driver.find_element(By.CLASS_NAME, 'iqOiiv').click()

    element = WebDriverWait(pytest.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[1]/div[3]/button/span')))
    pytest.driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div[3]/button/span').click()

    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.ID, 'address')))
    pytest.driver.find_element(By.ID, 'address').send_keys('89164112944')
    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.ID, 'otp_get_code')))
    pytest.driver.find_element(By.ID, 'otp_get_code').click()
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == 'Код подтверждения отправлен'

def test_authorization_by_code_change_number():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('89164112944')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('12qw!@QW')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'lk-btn')))
    pytest.driver.find_element(By.ID, 'lk-btn').click()
    element = WebDriverWait(pytest.driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, 'iqOiiv')))
    pytest.driver.find_element(By.CLASS_NAME, 'iqOiiv').click()

    element = WebDriverWait(pytest.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[1]/div[3]/button/span')))
    pytest.driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div[3]/button/span').click()

    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.ID, 'address')))
    pytest.driver.find_element(By.ID, 'address').send_keys('89164112944')
    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.ID, 'otp_get_code')))
    pytest.driver.find_element(By.ID, 'otp_get_code').click()

    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'otp-code-form__back-btn')))
    pytest.driver.find_element(By.CLASS_NAME, 'otp-code-form__back-btn').click()

def test_authorization_by_code_with_email():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('89164112944')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('12qw!@QW')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'lk-btn')))
    pytest.driver.find_element(By.ID, 'lk-btn').click()
    element = WebDriverWait(pytest.driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, 'iqOiiv')))
    pytest.driver.find_element(By.CLASS_NAME, 'iqOiiv').click()

    element = WebDriverWait(pytest.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[1]/div[3]/button/span')))
    pytest.driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div[3]/button/span').click()

    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.ID, 'address')))
    pytest.driver.find_element(By.ID, 'address').send_keys('mspromargo@gmail.com')
    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.ID, 'otp_get_code')))
    pytest.driver.find_element(By.ID, 'otp_get_code').click()
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == 'Код подтверждения отправлен'

def test_authorization_by_code_change_email():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('89164112944')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('12qw!@QW')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'lk-btn')))
    pytest.driver.find_element(By.ID, 'lk-btn').click()
    element = WebDriverWait(pytest.driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, 'iqOiiv')))
    pytest.driver.find_element(By.CLASS_NAME, 'iqOiiv').click()

    element = WebDriverWait(pytest.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[1]/div[3]/button/span')))
    pytest.driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div[3]/button/span').click()

    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.ID, 'address')))
    pytest.driver.find_element(By.ID, 'address').send_keys('mspromargo@gmail.com')
    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.ID, 'otp_get_code')))
    pytest.driver.find_element(By.ID, 'otp_get_code').click()

    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'otp-code-form__back-btn')))
    pytest.driver.find_element(By.CLASS_NAME, 'otp-code-form__back-btn').click()