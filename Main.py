from aiogram import Bot, Dispatcher
import asyncio
import Keys
from Handlers import router


async def main():
    try:
        bot = Bot(token=Keys.tg_token)
        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Error_in_Main: {e}")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot closed!")
