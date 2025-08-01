import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.dispatcher.webhook import get_new_configured_app
from aiogram.utils.executor import start_webhook
from image_generator import generate_image
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", default=5000))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("👋 077-Cypet-ке қош келдің!
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

🚀 Бастағың келсе — алғашқы сұранысыңды жаза бер!")

@dp.message_handler()
async def handle_prompt(message: types.Message):
    prompt = message.text
    await message.answer("Сурет генерациялануда, күте тұрыңыз")
    image_url = generate_image(prompt)
    if image_url:
        await message.answer_photo(photo=image_url)
    else:
        await message.answer("Өкінішке орай сурет генерацияланбады")

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == '__main__':
    from aiogram import executor
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

