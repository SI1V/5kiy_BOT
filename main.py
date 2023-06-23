from bs4 import BeautifulSoup
import requests
import os
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('API_5KIY_BOT'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.answer(f'С добром и любовью!\n{message.from_user.full_name}!!!\n'
                         f'Даты концертов взяты с официального сайта pyatnitsky.ru\n\n'
                         f'Чтобы просмотреть команды - выбери /help')
    

@dp.message_handler(commands=['help'])
async def command_start(message: types.Message):
    await message.answer(f'Концерты в Москве /mosconcert\n'
                         f'Концерты по России - /rusconcert\n'
                         f'Все концерты - /concerts')


@dp.message_handler(commands=['mosconcert'])
async def command_start(message: types.Message):
    url = 'https://pyatnitsky.ru/ru-afisha/ru-koncerty-v-moskve/'
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    date_concerts = soup.find_all("tbody")

    concert_info = "Концерты в Москве:\n_________________\n"

    for date_concert in date_concerts:
        rows = date_concert.find_all("tr")
        for row in rows:
            date_element = row.find('div', class_='date')
            date = date_element.b.text.strip()

            place_element = row.find('td', style='width: 56.1577%; height: 17px;')
            place_p_tags = place_element.find_all('p')

            cathedral_tag = place_p_tags[1]
            cathedral_text = cathedral_tag.text.strip() if cathedral_tag else ""

            concert_info += f"{date} - {cathedral_text}\n"

    concert_info += "_________________"
    await message.answer(concert_info)


@dp.message_handler(commands=['rusconcert'])
async def command_start(message: types.Message):
    url = 'https://pyatnitsky.ru/ru-afisha/ru-gastroli-v-rossii/'
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    date_concerts = soup.find_all("tbody")

    concert_info = "Концерты по России:\n_________________\n"

    for date_concert in date_concerts:
        rows = date_concert.find_all("tr")
        for row in rows:
            date_element = row.find('div', class_='date')
            date = date_element.b.text.strip()

            place_element = row.find('td', style='width: 56.1577%; height: 17px;')
            place_p_tags = place_element.find_all('p')

            place_tag = place_p_tags[0]
            place_text = place_tag.text.strip() if place_tag else ""

            concert_info += f"{date} - {place_text}\n"

    concert_info += "_________________"
    await message.answer(concert_info)


@dp.message_handler(commands=['concerts'])
async def command_start(message: types.Message):
    url = 'https://pyatnitsky.ru/ru-afisha/'
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    date_concerts = soup.find_all("tbody")

    concert_info = "Все концерты:\n_________________\n"

    for date_concert in date_concerts:
        rows = date_concert.find_all("tr")
        for row in rows:
            date_element = row.find('div', class_='date')
            date = date_element.b.text.strip()

            place_element = row.find('td', style='width: 56.1577%; height: 17px;')
            place_p_tags = place_element.find_all('p')

            place_tag = place_p_tags[0]
            place_text = place_tag.text.strip() if place_tag else ""

            concert_info += f"{date} - {place_text}\n"

    concert_info += "_________________"
    await message.answer(concert_info)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
