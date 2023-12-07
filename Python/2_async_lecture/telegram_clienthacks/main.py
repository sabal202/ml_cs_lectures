import asyncio
import random
import subprocess
from asyncio import sleep

import wikipediaapi  # pip install Wikipedia-API
from creds import api_hash, api_id
from heart import SLEEP, phase1, phase2, phase3, phase4
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait
from pyrogram.types import Message

app = Client("my_account", api_id=api_id, api_hash=api_hash)


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
            await sleep(e.value)


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
async def commands(_, msg: Message):
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
            await msg.edit(f"`{result.stdout}`", parse_mode=ParseMode.MARKDOWN)
        except:
            await msg.edit("`Команда завершена удачно`", parse_mode=ParseMode.MARKDOWN)
    else:
        await msg.edit(
            "`Я не могу выполнить эту команду`", parse_mode=ParseMode.MARKDOWN
        )


@app.on_message(filters.command("site", prefixes=".") & filters.me)
async def screenshot_site(_, msg: Message):
    to_send = msg.text.split(None, 1)
    # msg.delete()
    await app.send_photo(
        chat_id=msg.chat.id,
        photo=f"https://mini.s-shot.ru/1366x768/JPEG/1366/Z100/?{to_send[1]}",
    )


@app.on_message(filters.command("hack", prefixes=".") & filters.me)
async def hack(_, msg: Message):
    perc = 0

    while perc < 100:
        try:
            text = "👮‍ Взлом пентагона в процессе ..." + str(perc) + "%"
            await msg.edit(text)

            perc += random.randint(1, 3)
            await sleep(0.1)
        except FloodWait as e:
            await sleep(e.value)

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
            await sleep(e.value)

    await msg.edit("🦖 Найдены данные о существовании динозавров на земле!")


@app.on_message(filters.command("wiki", prefixes=".") & filters.me)
async def wiki(_, msg: Message):
    try:
        wiki_wiki = wikipediaapi.Wikipedia(
            language="ru", extract_format=wikipediaapi.ExtractFormat.WIKI
        )
        page_py = wiki_wiki.page(msg.text.split(None, 1))
        await msg.edit(f"`{page_py.summary}`", parse_mode=ParseMode.MARKDOWN)
    except:
        await msg.edit("По вашему запросу ничего не найдено")


if __name__ == "__main__":
    app.run()
