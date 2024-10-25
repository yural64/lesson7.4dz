from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def initialize_browser():
    # Инициализация драйвера (проверьте путь к драйверу, например, 'chromedriver.exe' для Windows)
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    return driver

def search_wikipedia(driver, query):
    driver.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)


def list_paragraphs(driver):
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")
    paragraph_counter = 0

    for paragraph in paragraphs:
        paragraph_text = paragraph.text.strip()  # Убираем лишние пробелы и переносы строк
        if paragraph_text:  # Если текст параграфа не пустой
            paragraph_counter += 1
            print(f"\n--- Параграф {paragraph_counter} ---\n{paragraph_text}")

            if paragraph_counter % 3 == 0:  # Предлагать дальнейшие действия после каждых 3 параграфов
                action = input("Введите 'n' для продолжения или 'q' для выхода в меню: ")
                if action.lower() == 'q':
                    break

def list_related_links(driver):
    links = driver.find_elements(By.CSS_SELECTOR, "#bodyContent a")
    related_links = [(index, link.text, link.get_attribute("href")) for index, link in enumerate(links) if link.text]
    for index, (text, href) in enumerate(related_links[:10]):
        print(f"{index + 1}. {text}")
    return related_links

def main():
    driver = initialize_browser()
    try:
        query = input("Введите запрос для поиска на Википедии: ")
        search_wikipedia(driver, query)

        while True:
            print("\nВыберите действие:\n1. Листать параграфы\n2. Перейти на связанную страницу\n3. Выйти")
            choice = input("Ваш выбор: ")

            if choice == "1":
                list_paragraphs(driver)
            elif choice == "2":
                related_links = list_related_links(driver)
                link_choice = int(input("Выберите номер связанной страницы для перехода: ")) - 1
                if 0 <= link_choice < len(related_links):
                    driver.get(related_links[link_choice][2])
                else:
                    print("Неверный выбор, попробуйте снова.")
            elif choice == "3":
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор, попробуйте снова.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
