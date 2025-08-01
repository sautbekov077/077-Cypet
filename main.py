import os
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web
from image_generator import generate_image
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer(
        """👋 077-Cypet-ке қош келдің!
Суреттерді жасайтын сенің жеке көмекшің 🎨

📸 Қиялыңды сипатта — мен соған сай сурет жасаймын.
Мысалы:
«Күн батқандағы футуристік қала, аниме стилінде»
немесе
«Ғарыштағы кішкентай мысық, шлеммен»

🛠 Мүмкіндіктері:
– Сипаттама арқылы сурет генерациясы
– Арт, фэнтези, реализм және басқа стильдер
– Қазақша және ағылшынша сұраныстарды қолдайды

🚀 Бастағың келсе — алғашқы сұранысыңды жаза бер!"""
    )

@dp.message()
async def handle_prompt(message: Message):
    prompt = message.text
    await message.answer("Сурет генерациялануда, күте тұрыңыз...")
    image_url = generate_image(prompt)
    if image_url:
        await message.answer_photo(image_url)
    else:
        await message.answer("Өкінішке орай сурет генерацияланбады 😢")

async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()

async def main():
    app = web.Application()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_router(dp)
    setup_application(app, dp, bot=bot)
    return app

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    web.run_app(main(), host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
