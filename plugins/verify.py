# Updated verify.py - Fast Verification System
# Don't Remove Credit Tg - @VJ_Botz

import time
from info import *
from utils import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("verify") & filters.group)
async def verify_user(bot, message):
    user_id = message.from_user.id
    
    # Check if user is already verified
    if await is_user_verified(user_id):
        return await message.reply_text(f"<b>✅ Hey {message.from_user.mention}, You are already verified!</b>")

    # Verification Link Generation (Agar aap Shortener use kar rahe hain)
    # Agar shortener nahi hai toh ye basic verification dikhayega
    m = await message.reply_text("🔄 **Generating Verification Link...**")
    
    try:
        # Aapki website ya shortener ka link yahan logic mein aata hai
        # Abhi ke liye hum simple verification status check rakh rahe hain
        verify_link = f"https://t.me/{bot.me.username}?start=verify_{user_id}"
        
        buttons = [
            [InlineKeyboardButton("🔐 Click Here To Verify", url=verify_link)],
            [InlineKeyboardButton("❓ How To Verify", url="https://t.me/VJ_Botz")] # Aapna tutorial link dalein
        ]
        
        await m.edit(
            text=f"<b>👋 Hello {message.from_user.mention},\n\nAapko search results dekhne ke liye verify karna hoga.\n\nNiche diye gaye button par click karein:</b>",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        await m.edit(f"<b>❌ Error:</b> `{e}`")

@Client.on_message(filters.command("id"))
async def get_id(bot, message):
    # Useful command to get Group or User ID
    text = f"<b>👤 User ID:</b> `{message.from_user.id}`\n"
    if message.chat.type != "private":
        text += f"<b>👥 Group ID:</b> `{message.chat.id}`"
    await message.reply_text(text)
    
