import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from openai import OpenAI
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация OpenAI клиента для OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key='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'
)

# Инициализация бота
API_TOKEN = '7881628999:AAFKXjjguh6oLR-wD7sQbfWxMx8tWLVPFb8'
from aiogram.client.default import DefaultBotProperties

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Обработчик команды /start
from aiogram.filters import Command


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для сравнения характеристик телефонов. "
                        "Напиши мне названия двух телефонов, например: 'iPhone 14 и Galaxy S23', "
                        "и я сравню их характеристики, плюсы и минусы.")


# Обработчик текстовых сообщений
@dp.message()
async def compare_phones(message: types.Message):
    user_input = message.text

    # Проверяем, содержит ли сообщение ключевые слова для сравнения
    if " и " in user_input or " vs " in user_input.lower():
        await message.reply("Сравниваю телефоны, пожалуйста подождите...")

        try:
            # Запрос к OpenRouter API
            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://t.me/YourBotName",
                    "X-Title": "Phone Comparison Bot",
                },
                extra_body={},
                model="google/gemini-2.0-flash-exp:free",
                messages=[
                    {
                        "role": "user",
                        "content": f"""Сравни два смартфона: {user_input}.
1. Дай основные характеристики (экран, процессор, камера, батарея, память, ОС и т.п.).
2. Укажи сильные и слабые стороны каждого.
3. Структурируй в виде списков, можно использовать emoji (✔️, ❌, 🔋 и т.п.).
4. Сделай вывод: какой телефон лучше и кому подойдёт.
⚠️ Не используй кавычки ("", '', «», „“ и т.п.) вообще — ни в названиях, ни в заголовках.
Пиши как Telegram-сообщение: с простыми заголовками, списками, без форматирования Markdown или HTML.
Язык — русский. Стиль — простой и понятный, без перегруженности терминами."""
                    }
                ]
            )

            response = completion.choices[0].message.content
            cleaned = response.replace('"', '').replace("«", "").replace("»", "").replace("“", "").replace("”",
                                                                                                           "").replace(
                "‘", "").replace("’", "")
            # Разбиваем длинный ответ на части
            for i in range(0, len(response), 4096):
                await message.reply(response[i:i + 4096])

        except Exception as e:
            logging.error(f"Error: {e}")
            await message.reply("Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.")
    else:
        await message.reply(
            "Пожалуйста, укажите два телефона для сравнения через 'и' или 'vs', например: 'iPhone 14 и Galaxy S23'")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
