# Updated connect.py - Professional & Fast Connection Logic
# Don't Remove Credit Tg - @VJ_Botz

from info import *
from utils import *
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.group & filters.command("connect") & filters.user(ADMIN))
async def connect(bot, message):
    if len(message.command) < 2:
        return await message.reply_text("<b>⚠️ Usage:</b> `/connect -100xxxxxxxxxx` (Channel ID)")
    
    group_id = message.chat.id
    channel_id = message.command[1]
    
    # Check if ID is valid
    if not channel_id.startswith("-100"):
        return await message.reply_text("<b>❌ Invalid ID!</b> Make sure it starts with `-100`")

    m = await message.reply_text("🔄 **Connecting Channel...**")
    
    try:
        # Check if Bot is Admin in that channel
        chat = await bot.get_chat(channel_id)
        status = await add_channel(group_id, channel_id) # Using utils function
        
        if status:
            await m.edit(f"<b>✅ Successfully Connected!</b>\n\n<b>Channel:</b> `{chat.title}`\n<b>ID:</b> `{channel_id}`\n\nNow I will search posts from this channel in this group.")
        else:
            await m.edit("<b>⚠️ This channel is already connected to this group!</b>")
            
    except Exception as e:
        await m.edit(f"<b>❌ Connection Failed!</b>\n\n<b>Error:</b> `{e}`\n\n<b>Make sure:</b>\n1. Bot is Admin in Channel.\n2. Channel ID is correct.")

@Client.on_message(filters.group & filters.command("disconnect") & filters.user(ADMIN))
async def disconnect(bot, message):
    group_id = message.chat.id
    m = await message.reply_text("🔄 **Disconnecting...**")
    
    status = await remove_group(group_id) # Clears all connections for this group
    
    if status:
        await m.edit("<b>✅ All channels disconnected from this group!</b>")
    else:
        await m.edit("<b>❌ No channels were connected to this group.</b>")

@Client.on_message(filters.group & filters.command("connections") & filters.user(ADMIN))
async def connections(bot, message):
    group_id = message.chat.id
    group_data = await get_group(group_id)
    channels = group_data.get("channels", [])

    if not channels:
        return await message.reply_text("<b>❌ No channels connected to this group!</b>")

    text = "<b>📂 Connected Channels:</b>\n\n"
    for count, channel in enumerate(channels, 1):
        try:
            chat = await bot.get_chat(channel)
            text += f"{count}. <code>{chat.title}</code> (<code>{channel}</code>)\n"
        except:
            text += f"{count}. <code>Unknown Channel</code> (<code>{channel}</code>)\n"

    await message.reply_text(text)
    
