import asyncio
import telegram

async def main():
    bot = telegram.Bot("5736217621:AAGcn1-HYmlXDECwjdo9h7s1A6mEu4Ub9lc")
    async with bot:
        await bot.send_message(text="Tạo bot thành công", chat_id=5064447056)

if __name__ == '__main__':
    asyncio.run(main())