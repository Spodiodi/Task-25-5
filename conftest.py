import uuid

import chromedriver_autoinstaller
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Для пользователей Windows
chromedriver_autoinstaller.install()


@pytest.fixture
def driver():
    #driver = webdriver.Chrome(service='C:\\Kibizova\\WebDriver\\chrome-win64\\chromedriver.exe')
    service = Service(executable_path="C:\\Kibizova\\WebDriver\\chrome-win64\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    # Можно задавать нужный вам размер экрана
    # driver.set_window_size(1080, 800)

    # driver.maximize_window()
    return driver


@pytest.fixture
def web_browser(request, driver):

    browser = driver
    browser.set_window_size(1400, 1000)

    # Вернуть объект браузера
    yield browser

    # Этот код выполнится после отрабатывания теста:
    if request.node.rep_call.failed:
        # Сделать скриншот, если тест провалится:
        browser.execute_script("document.body.bgColor = 'white';")

        # Создаем папку screenshots и кладем туда скриншот с генерированным именем:
        browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

        # Для дебагинга, печатаем информацию в консоль
        print('URL: ', browser.current_url)
        print('Browser logs:')
        for log in browser.get_log('browser'):
            print(log)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep
