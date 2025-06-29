from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from Client import client

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.reply("Привет! Я бот для сравнения характеристик телефонов. "
                        "Напиши мне названия двух телефонов, например: 'iPhone 14 и Galaxy S23', "
                        "и я сравню их характеристики, плюсы и минусы.")


@router.message()
async def compare_phones(message: Message):
    user_input = message.text

    if " и " in user_input.lower() or " vs " in user_input.lower():
        await message.reply("Сравниваю телефоны, пожалуйста подождите...")

        try:

            prompt = client.chat.completions.create(
                model="deepseek/deepseek-chat-v3-0324:free",
                messages=[{
                    "role": "user",
                    "content": f"""Сравни два смартфона: {user_input}.
                1. Дай основные характеристики (экран, процессор, камера, батарея, память, ОС и т.п.).
                2. Укажи сильные и слабые стороны каждого.
                3. Структурируй в виде списков, можно использовать emoji (✅, ❌, 🔋 и т.п.).
                4. Сделай вывод: какой телефон лучше и кому подойдёт.
                ⚠️ Не используй кавычки ("", '', *, #, «», „“ и т.п.) вообще — ни в названиях, ни в заголовках.
                Пиши как Telegram-сообщение: с простыми заголовками, списками, без форматирования Markdown или HTML.
                Язык — русский. Стиль — простой и понятный, без перегруженности терминами.
                Если в сравнении неизвестные тебе модели телефонов пиши что я не знаю такие
                модели и не могу их сравнить."""
                }])

            response = prompt.choices[0].message.content
            cleaned = (response.replace('"', '').replace("«", "").replace
                       ("»", "").replace("“", "").replace("”", "").replace(
                "‘", "").replace("’", "").replace("###", "").
                       replace("####", "").replace("**", "").replace("#", ""))

            for i in range(0, len(cleaned), 4096):
                await message.answer(cleaned[i:i + 4096])

        except Exception as e:
            print(f"Error_in_Handlers: {e}")
            await message.reply("Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.")
    else:
        await message.reply(
            "Пожалуйста, укажите два телефона для сравнения через 'и' или 'vs', например: 'iPhone 14 и Galaxy S23'")
