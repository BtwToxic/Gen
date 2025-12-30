import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import (
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
)
from pyromod import listen
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = "8094733589:AAGg3nkrh8yT6w5C7ySbV7C54bE5n6lyeCg"
API_ID = 21705136
API_HASH = "78730e89d196e160b0f1992018c6cb19"

bot = Client(
    "string_gen_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
)

@bot.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply_text(
        "**Pyrogram String Session Generator**❤️‍🩹\n\n"
        "Use /gen to create your string session.\n\n"
        "⚠️ Never share your string with anyone.\n\n"
        "**Join ~** @TechBotss\n\n"
        "**Developer** ~ @ikBug"
    )

@bot.on_message(filters.command("gen"))
async def generate(_, msg):
    user = msg.from_user.id

    phone = await msg.chat.ask(
        "📱 Send your phone number with country code\n\nExample: `+911234567890`",
        timeout=300
    )

    client = Client(
        name="user_session",
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True,
    )

    await client.connect()

    try:
        sent = await client.send_code(phone.text)
    except Exception as e:
        await msg.reply_text(f"Failed to send OTP\n\n`{e}` Please Try Again")
        return

    otp = await msg.chat.ask(
        "🔐 Enter OTP\n\nExample: `1 2 3 4 5`",
        timeout=300
    )

    try:
        await client.sign_in(
            phone.text,
            sent.phone_code_hash,
            otp.text.replace(" ", "")
        )
    except PhoneCodeInvalid:
        return await msg.reply_text("Invalid OTP")
    except PhoneCodeExpired:
        return await msg.reply_text("OTP expired")
    except SessionPasswordNeeded:
        pwd = await msg.chat.ask(
            "🔑 2-Step Verification enabled\n\nSend your password:",
            timeout=300
        )
        try:
            await client.check_password(pwd.text)
        except PasswordHashInvalid:
            return await msg.reply_text("Wrong password")

    string = await client.export_session_string()
    await client.disconnect()

    await msg.reply_text(
        "🌷 **String Session Generated**\n\n"
        f"`{string}`\n\n"
        "⚠️ Keep it private!\n\n Don't Share With Your Girlfriend ❤️‍🩹🌚",
        quote=True
    )

bot.run()
