# Updated misc.py - Help & Start Logic
# Don't Remove Credit Tg - @VJ_Botz

from info import *
from utils import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("start") & filters.private)
async def start(bot, message):
    # Add user to database if not exists
    await add_user(message.from_user.id)
    
    buttons = [
        [
            InlineKeyboardButton("➕ Add Me To Your Group", url=f"http://t.me/{bot.me.username}?startgroup=true")
        ],
        [
            InlineKeyboardButton("🛠 Help", callback_data="help"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
        [
            InlineKeyboardButton("🎬 Join Channel", url="https://t.me/VJ_Botz")
        ]
    ]
    
    await message.reply_photo(
        photo="https://graph.org/file/c361a803c7b70fc50d435.jpg", # Aap apni image URL yahan dal sakte hain
        caption=f"<b>👋 Hello {message.from_user.mention}!\n\nMain ek Advance Telegram Post Search Bot hoon.\n\nMujhe apne group mein add karein aur apne channels connect karke search feature ka maza lein.</b>",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex("help"))
async def help_cb(bot, query):
    text = (
        "<b>📖 Bot Kaise Use Karein?</b>\n\n"
        "1. Bot ko apne Group mein <b>Admin</b> banayein.\n"
        "2. Bot ko apne Channel mein bhi <b>Admin</b> banayein.\n"
        "3. Group mein command dein: `/connect -100xxxxxxxx` (Channel ID).\n"
        "4. Bas! Ab group mein movie ya post ka naam likhein, main dhundh nikalunga."
    )
    buttons = [[InlineKeyboardButton("🔙 Back", callback_data="start_back")]]
    await query.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex("about"))
async def about_cb(bot, query):
    text = (
        "<b>🤖 Bot Info:</b>\n"
        "• <b>Name:</b> Post Search Bot\n"
        "• <b>Language:</b> Python 3\n"
        "• <b>Library:</b> Pyrogram\n"
        "• <b>Channel:</b> @VJ_Botz"
    )
    buttons = [[InlineKeyboardButton("🔙 Back", callback_data="start_back")]]
    await query.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex("start_back"))
async def start_back(bot, query):
    # Wapas start menu par le jane ke liye
    buttons = [
        [InlineKeyboardButton("➕ Add Me To Your Group", url=f"http://t.me/{bot.me.username}?startgroup=true")],
        [InlineKeyboardButton("🛠 Help", callback_data="help"), InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ]
    await query.message.edit_caption(
        caption=f"<b>👋 Welcome Back {query.from_user.mention}!</b>",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    
