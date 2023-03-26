import asyncio
import random
import subprocess
from asyncio import sleep

import requests
import wikipediaapi  # pip install Wikipedia-API
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import ChatPermissions, Message

from creds import api_hash, api_id
from heart import phase1, phase2, phase3, phase4, _wrap_edit, SLEEP

app = Client("my_account", api_id=api_id, api_hash=api_hash)

# Команда type
@app.on_message(filters.command("type", prefixes=".") & filters.me)
async def type(_, msg: Message):
    orig_text = msg.text.split(".type ", maxsplit=1)[1]
    text = orig_text
    tbp = ""  # to be printed
    typing_symbol = "▒"
    while tbp != orig_text:
        try:
            await msg.edit(tbp + typing_symbol)
            await sleep(0.01)  # 10 ms

            tbp = tbp + text[0]
            text = text[1:]

            await msg.edit(tbp)
            await sleep(0.01)

        except FloodWait as e:
            await sleep(e.x)


@app.on_message(filters.command("magic", prefixes=".") & filters.me)
async def hearts(_, message: Message):
    await phase1(message)
    await phase2(message)
    await phase3(message)
    await phase4(message)
    await asyncio.sleep(SLEEP * 3)

    final_caption = " ".join(message.command[1:])
    if not final_caption:
        final_caption = "💕"
    await message.edit(final_caption)


@app.on_message(filters.command("cm", prefixes=".") & filters.me)
async def commands(_, msg):
    to_send = msg.text.split(None, 1)
    result = subprocess.run(
        to_send[1],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        encoding="utf-8",
    )
    if result.returncode == 0:
        try:
            await msg.edit(f"`{result.stdout}`", parse_mode="MARKDOWN")
        except:
            await msg.edit("`Команда завершена удачно`", parse_mode="MARKDOWN")
    else:
        await msg.edit("`Я не могу выполнить эту команду`", parse_mode="MARKDOWN")


@app.on_message(filters.command("site", prefixes=".") & filters.me)
async def screenshot_site(_, msg):
    to_send = msg.text.split(None, 1)
    # msg.delete()
    await app.send_photo(
        chat_id=msg.chat.id,
        photo=f"https://mini.s-shot.ru/1366x768/JPEG/1366/Z100/?{to_send[1]}",
    )


@app.on_message(filters.command("search", prefixes=".") & filters.me)
async def search_google(_, msg):
    user_agent = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
    }

    to_send = msg.text.split(None, 1)  # Запрашиваем у юзера, что он хочет найти
    url = requests.get(
        f"https://www.google.com/search?q={to_send[1]}", headers=user_agent
    )
    soup = BeautifulSoup(url.text, features="lxml")  # Получаем запрос
    r = soup.find_all("div", class_="yuRUbf")  # Выводи весь тег div class="r"
    rs = soup.find_all("div", class_="IsZvec")
    results_news = []
    for s, sr in zip(r, rs):
        link = s.find("a").get("href")  # Ищем ссылки по тегу <a href="example.com"
        title = s.find("h3")  # Ищем описание ссылки по тегу <h3 class="LC20lb DKV0Md"
        opisanie = sr.get_text()
        title = title.get_text()
        results = f'<a href="{link}">{title}</a>\n<code>{opisanie}</code>'
        results_news.append(results)
        result = "\n\n".join(results_news)

    await msg.edit(
        f'Результаты по запросу: `"{to_send[1]}"`\n\n{result}',
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


@app.on_message(filters.command("hack", prefixes=".") & filters.me)
async def hack(_, msg):
    perc = 0

    while perc < 100:
        try:
            text = "👮‍ Взлом пентагона в процессе ..." + str(perc) + "%"
            await msg.edit(text)

            perc += random.randint(1, 3)
            await sleep(0.1)

        except FloodWait as e:
            await sleep(e.x)

    await msg.edit("🟢 Пентагон успешно взломан!")
    await sleep(3)

    await msg.edit("👽 Поиск секретных данных об НЛО ...")
    perc = 0

    while perc < 100:
        try:
            text = f"👽 Поиск секретных данных об НЛО ...{perc}%"
            await msg.edit(text)

            perc += random.randint(1, 5)
            await sleep(0.15)

        except FloodWait as e:
            await sleep(e.x)

    await msg.edit("🦖 Найдены данные о существовании динозавров на земле!")


@app.on_message(filters.command("wiki", prefixes=".") & filters.me)
async def wiki(_, msg):
    try:
        wiki_wiki = wikipediaapi.Wikipedia(
            language="ru", extract_format=wikipediaapi.ExtractFormat.WIKI
        )
        page_py = wiki_wiki.page(msg.text.split(None, 1))
        await msg.edit(f"`{page_py.summary}`", parse_mode="MARKDOWN")

    except:
        await msg.edit("По вашему запросу ничего не найдено")


app.run()
