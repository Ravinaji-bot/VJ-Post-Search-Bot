import asyncio
from info import *
from utils import *
from time import time 
from plugins.generate import database
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message 
from pyrogram.errors import FloodWait

# Global variable to store session to avoid multiple connects
USER_BOT = None

async def get_user_bot():
    global USER_BOT
    if USER_BOT:
        return USER_BOT
    vj = database.find_one({"chat_id": ADMIN})
    if vj:
        USER_BOT = Client("post_search", session_string=vj['session'], api_hash=API_HASH, api_id=API_ID)
        await USER_BOT.start()
        return USER_BOT
    return None

async def delete_after_delay(message: Message, delay):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except:
        pass

@Client.on_message(filters.text & filters.group & filters.incoming & ~filters.command(["verify", "connect", "id"]))
async def search(bot, message):
    if message.text.startswith("/"):
        return
        
    f_sub = await force_sub(bot, message)
    if not f_sub:
        return     

    group_data = await get_group(message.chat.id)
    channels = group_data.get("channels", [])
    if not channels:
        return     

    user_bot = await get_user_bot()
    if not user_bot:
        return await message.reply("<b>⚠️ Admin Session Not Found! Please Login first.</b>")

    query = message.text 
    m = await message.reply("🔍 **Searching your request... Please wait.**")
    
    results = ""
    found_names = set() # To avoid duplicates efficiently
    
    try:
        # Searching across all channels in parallel for speed
        tasks = []
        for channel in channels:
            tasks.append(user_bot.search_messages(chat_id=channel, query=query))
        
        for task in tasks:
            async for msg in task:
                text = msg.text or msg.caption
                if not text: continue
                name = text.split("\n")[0]
                if name not in found_names:
                    found_names.add(name)
                    results += f"<b>🎬 {name}</b>\n🔗 [Get File From Here]({msg.link})\n\n"

        if not results:
            await m.delete()
            movies = await search_imdb(query)
            buttons = [[InlineKeyboardButton(movie['title'], callback_data=f"recheck_{movie['id']}")] for movie in movies]
            return await message.reply_photo(
                photo="https://graph.org/file/c361a803c7b70fc50d435.jpg",
                caption="<b>❌ Result Not Found!\n\n💡 Did you mean any of these? Select below:</b>", 
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        
        await m.delete()
        head = f"<b>👋 Hey {message.from_user.mention},\n✅ Your Results are Ready:</b>\n\n"
        footer = "\n<b>⚡ Powered By @Gajab_Facts_Gujarati</b>" # Aapka channel name
        
        final_text = head + results + footer
        
        # Split into chunks if text is too long
        for i in range(0, len(final_text), 4096):
            sent_msg = await bot.send_message(chat_id=message.chat.id, text=final_text[i:i+4096], disable_web_page_preview=True)
            asyncio.create_task(delete_after_delay(sent_msg, 300)) # Delete after 5 mins for clean group

    except Exception as e:
        print(f"Error: {e}")
        await m.edit("<b>❌ Something went wrong while searching.</b>")

@Client.on_callback_query(filters.regex(r"^recheck"))
async def recheck(bot, update):
    user_bot = await get_user_bot()
    if not user_bot:
        return await update.answer("Admin not logged in!", show_alert=True)

    # Security Check
    try:
        if update.from_user.id != update.message.reply_to_message.from_user.id:
            return await update.answer("This is not for you! ✋", show_alert=True)
    except: pass

    await update.message.edit("<b>🚀 Re-searching with IMDb data...</b>")
    movie_id = update.data.split("_")[-1]
    query = await search_imdb(movie_id)
    
    channels = (await get_group(update.message.chat.id))["channels"]
    results = ""
    found_names = set()

    async for msg in user_bot.search_messages(chat_id=channels[0], query=query): # Example for first channel
        text = msg.text or msg.caption
        if not text: continue
        name = text.split("\n")[0]
        if name not in found_names:
            found_names.add(name)
            results += f"<b>🎬 {name}</b>\n🔗 {msg.link}\n\n"

    if not results:
        return await update.message.edit("<b>🔺 Still nothing found! Requesting to Admin...</b>", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎯 Request Admin", callback_data=f"request_{movie_id}")]]))
    
    await update.message.delete()
    sent_msg = await bot.send_message(update.message.chat.id, f"<b>✅ Found results for '{query}':</b>\n\n{results}")
    asyncio.create_task(delete_after_delay(sent_msg, 300))
        
