# Updated fsub.py - Optimized for Speed
# Don't Remove Credit Tg - @VJ_Botz

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from info import FSUB_ID, AUTH_CHANNEL # Make sure these are in your info.py

async def force_sub(bot, message):
    # Agar FSUB_ID set nahi hai toh bypass karein
    if not FSUB_ID:
        return True
        
    try:
        # Check if user is a participant
        user = await bot.get_chat_member(FSUB_ID, message.from_user.id)
        if user.status == "kicked":
            await message.reply_text("❌ Sorry, You are Banned from using me.")
            return False
        return True
    except UserNotParticipant:
        # User ne join nahi kiya, toh button dikhayein
        try:
            invite_link = await bot.create_chat_invite_link(FSUB_ID)
        except:
            invite_link = await bot.get_chat(FSUB_ID)
            invite_link = invite_link.invite_link

        buttons = [
            [InlineKeyboardButton("📢 Join Channel", url=invite_link.invite_link if hasattr(invite_link, 'invite_link') else invite_link)]
        ]
        
        # Try again button adding for better UX
        buttons.append([InlineKeyboardButton("🔄 Try Again", url=f"https://t.me/{bot.me.username}?start=start")])

        await message.reply_text(
            text=f"<b>👋 Hello {message.from_user.mention},\n\nYou must join our channel to use this bot. Click the button below to join!</b>",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return False
    except Exception as e:
        print(f"Error in FSub: {e}")
        return True # Error aane par block na karein
