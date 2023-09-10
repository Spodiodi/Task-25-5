import time

from selenium.webdriver.common.by import By


def test_search_example(driver):
    """ Поиск текста в google, далее делаем скриншот страницы. """

    # Открываем страницу для поиска:
    driver.get('https://google.com')

    time.sleep(10)  # небольшая задержка, чисто ради эксперимента

    # Поиск элемента для ввода текста:
    search_input = driver.find_element(By.NAME, 'q')

    # Очистка поля, далее ввод текста для поиска:
    search_input.clear()
    search_input.send_keys('first test')

    time.sleep(10)  # небольшая задержка, чисто ради эксперимента

    # Поиск элемента "кнопка", далее нажатие на кнопку:
    search_button = driver.find_element(By.NAME, "btnK")
    search_button.submit()

    time.sleep(10)  # небольшая задержка, чисто ради эксперимента

    # Сохранение скриншота
    driver.save_screenshot('result.png')
