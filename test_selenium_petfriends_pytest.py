import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_url = "https://petfriends.skillfactory.ru"


@pytest.fixture
def test_pet_friends(web_browser):
    driver = web_browser
    # Открыть домашнюю страницу PetFriends:
    driver.get(base_url)

    time.sleep(5)  # небольшая задержка, чисто ради эксперимента

    # Находим кнопку "Зарегистрироваться" и нажимаем на нее
    btn_newuser = driver.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")
    btn_newuser.click()

    # Ищем надпись "У меня уже есть аккаунт" и нажимаем на нее
    btn_exist_acc = driver.find_element(By.LINK_TEXT, u"У меня уже есть аккаунт")
    btn_exist_acc.click()

    # Ищем поле ввода электронной почты, очищаем его, а затем вводим свой email,
    # подставить вместо "<your_email>" свой email.
    field_email = driver.find_element(By.ID, "email")
    field_email.clear()
    field_email.send_keys("natashas@mail.com")

    # То же самое для поля с паролем
    field_pass = driver.find_element(By.ID, "pass")
    field_pass.clear()
    field_pass.send_keys("12345")

    # Ищем кнопку "Войти" и нажимаем на нее
    btn_submit = driver.find_element(By.XPATH, "//button[@type='submit']")
    btn_submit.click()

    time.sleep(5)  # небольшая задержка, чисто ради эксперимента

    if driver.current_url == f'{base_url}/all_pets':
        # Если мы на странице отображения моих питомцев, то сделать скриншот
        driver.save_screenshot('result_petfriends.png')
    else:
        raise Exception("login error")


def test_show_all_pets(driver):
    # Переходим на страницу авторизации
    driver.get(f'{base_url}/login')
    # Вводим email
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    driver.find_element(By.ID, 'email').send_keys('natashas@mail.com')
    # Вводим пароль
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # добавляем неявное ожидание получения списка карточек
    driver.implicitly_wait(10)
    # фотографии питомцев
    images = driver.find_elements(By.XPATH, '//img[@class="card-img-top"]')
    # имена питомцев
    names = driver.find_elements(By.XPATH, '//h5[@class="card-title"]')
    # описания питомцев
    descriptions = driver.find_elements(By.XPATH, '//p[@class="card-text"]')
    # в цикле перебираем элементы наших списков полученных с сайта карточек питомцев
    for i in range(len(names)):
        #  Потому что на сайте https://petfriends.skillfactory.ru/all_pets не все питомцы имеют полностью
        #  заполненную информацию (имя, порода, возраст, изображение), проверки будут падать.
        #  но можно вместо len(names) - то есть количества всех питомцев на странице ,
        #  можно вставить меньшее количество питомцев для проверки, к примеру 1 или 2 и прогнать тест.

        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i].text
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_my_pet_table(test_pet_friends, web_browser):
    # залогинимся через другой тест, используя фикстуру
    driver = web_browser
    # Открыть домашнюю страницу PetFriends:
    driver.get(f'{base_url}/my_pets')
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class=".col-sm-4 '
                                                                                        'left"]/h2')))
    print(element.text)
    assert element
'''
    # имена питомцев
    names = driver.find_elements(By.XPATH, '//h5[@class="card-title"]')
    # количество питомцев
    text = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]/text()[1]')
    print(text)
'''
