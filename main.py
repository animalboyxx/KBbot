from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import telebot

bot = telebot.TeleBot('6288158606:AAHPxgELrGUuGnqiyznnntdCFI82zxIIGCg')


@bot.message_handler(func=lambda message: True)
def drinks(message):
    global iskomoe
    iskomoe = message.text
    print(iskomoe)
    #print(pr(iskomoe))
    bot.reply_to(message, '\n'.join(pr(iskomoe)))


def pr(iskomoe):
    browser = webdriver.Chrome()
    #options = webdriver.ChromeOptions()
    browser.maximize_window()  # во весь экран
    browser.get("https://krasnoeibeloe.ru/")
    action = ActionChains(browser)
    action.move_to_element(browser.find_element(By.CLASS_NAME,
                                                'top_line_at_wrap'))  # перевожу курсор на элемент что бы спровоцировать появление возрастного аппрува
    action.perform()
    time.sleep(1)
    age_approve = browser.find_element(By.XPATH,
                                       '//*[@id="age_popup_container"]/div[2]/div[2]/a[1]')  # возрастной аппрув
    age_approve.click()
    time.sleep(1)
    search_input = browser.find_element(By.ID, 'title-search-input')  # ввод искомого
    search_input.send_keys(iskomoe)
    search_button = browser.find_element(By.XPATH, '//*[@id="search"]/form/div/input[2]')
    search_button.click()  # нажатие кнопки поиска
    items = []
    products = browser.find_elements(By.CLASS_NAME, "catalog_products_block")
    names = browser.find_elements(By.CLASS_NAME, 'catalog_products_block')
    i = 0
    j = 0
    while i <= len(products):
        for name in names:
            items.append(name.text)
            i += 1

    elements_w_prices = items[0].split('\n')  # список с наименованиям
    index_list = []  # лист индексов
    while j < len(elements_w_prices):  # поиск индексов элементов с ценой
        if elements_w_prices[j].find("₽") != -1:  # если в строке присутствует элемент
            index_list.append(j)  # добавляю индекс элемента в лист
        j += 1

    elements_cleaned = []  # очищенный лист элементов
    gg = 0
    spase_symbol = ' '
    while gg < len(
            index_list):  # здесь беру элемент, содержащий цену, и перед ним ставлю два элемента с остальной информацией
        first_s_deleted = elements_w_prices[index_list[gg]]
        first_s_deleted = first_s_deleted[1:]
        elements_cleaned.append(
            elements_w_prices[index_list[gg] - 2] + spase_symbol + elements_w_prices[
                index_list[gg] - 1] + spase_symbol +
            elements_w_prices[index_list[gg]])  # склеиваю те элементы, которые обладают ценой
        gg += 1

    if len(elements_cleaned) > 0:
        return elements_cleaned
    else:
        return ['List is empty']


if __name__ == '__main__':
    bot.polling()
