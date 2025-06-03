import asyncio
from aiogram import Bot, Dispatcher
import Keys
from Handlers import router
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


async def main():
    bot = Bot(
        token=Keys.tg_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot closed!")
