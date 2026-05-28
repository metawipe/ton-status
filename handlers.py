from groq import AsyncGroq
from config import GROQ_API_KEY
from keyboards import make_keyboard
from prompt import get_system_prompt
from ton_api import get_ton_data
from utils import (
    HELP_TEXT,
    ERROR_TEXT,
    get_ton_amount,
)

keyboard = make_keyboard()
groq = AsyncGroq(api_key=GROQ_API_KEY)


def make_course_text(data):
    usd_price = data["prices"]["USD"]
    rub_price = data["prices"]["RUB"]
    change_24h = data["diff_24h"]["USD"]
    change_7d = data["diff_7d"]["USD"]
    return (
        f"💎 TON: ${usd_price:.2f} | {rub_price:.2f} ₽\n"
        f"📊 24ч: {change_24h:.2f}%\n"
        f"📊 7д: {change_7d:.2f}%"
    )


def make_converter_text(amount, data):
    usd_price = data["prices"]["USD"]
    rub_price = data["prices"]["RUB"]
    total_usd = amount * usd_price
    total_rub = amount * rub_price
    return (
        f"💱 {amount} TON = ${total_usd:.2f}\n"
        f"💵 {amount} TON = {total_rub:.2f} ₽\n"
        f"📌 1 TON = ${usd_price:.2f} | {rub_price:.2f} ₽"
    )


def make_ai_text(data):
    usd_price = data["prices"]["USD"]
    change_24h = data["diff_24h"]["USD"]
    change_7d = data["diff_7d"]["USD"]
    return (
        f"Курс TON: ${usd_price:.2f}. "
        f"Изменение за 24 часа: {change_24h:.2f}%. "
        f"Изменение за 7 дней: {change_7d:.2f}%."
    )


def register_handlers(bot):
    @bot.on.private_message(text=["Курс", "курс"])
    async def send_course(message):
        data = get_ton_data()
        if data is None:
            await message.answer(ERROR_TEXT)
            return
        await message.answer(make_course_text(data), keyboard=keyboard)

    @bot.on.private_message(text=["Анализ", "анализ"])
    async def send_analysis(message):
        data = get_ton_data()
        if data is None:
            await message.answer(ERROR_TEXT)
            return

        answer = await groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": get_system_prompt(),
                },
                {
                    "role": "user",
                    "content": make_ai_text(data),
                },
            ],
        )
        prediction = answer.choices[0].message.content
        await message.answer(f"🧠 Анализ TON:\n\n{prediction}", keyboard=keyboard)

    @bot.on.private_message(text=["Конвертер", "конвертер"])
    async def send_converter_help(message):
        await message.answer(
            'Напиши количество TON.\nНапример:\n"10 TON"', keyboard=keyboard
        )

    @bot.on.private_message()
    async def send_default(message):
        amount = get_ton_amount(message.text)
        if amount is not None:
            data = get_ton_data()
            if data is None:
                await message.answer(ERROR_TEXT)
                return
            await message.answer(make_converter_text(amount, data), keyboard=keyboard)
            return

        await message.answer(HELP_TEXT, keyboard=keyboard)
