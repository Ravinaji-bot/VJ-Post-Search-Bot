# Updated info.py - Optimized for @VJ_Botz Structure
# Don't Remove Credit Tg - @VJ_Botz

import os
from os import environ

# --- Bot Account Settings ---
API_ID       = int(environ.get("API_ID", "24358501"))
API_HASH     = environ.get("API_HASH", "fa51ce8876c215d8a76c98c755e6d2d3")
BOT_TOKEN    = environ.get("BOT_TOKEN", "") # Apna Token Dalein

# --- Database & Logs ---
DATABASE_URI = environ.get("DATABASE_URI", "") # Apna MongoDB Link Dalein
LOG_CHANNEL  = int(environ.get("LOG_CHANNEL", "-1002371873191"))
ADMIN        = int(environ.get("ADMIN", "6522113087"))

# --- Channel & Subscription ---
# Iska use fsub.py aur search.py mein hoga
CHANNEL      = environ.get("CHANNEL", "@et3tvwtwtjs")
FSUB_ID      = int(environ.get("FSUB_ID", "-1002371873191")) # Force Sub ID yahan dalein

# --- UI & Design Settings ---
START_IMG    = "https://graph.org/file/c361a803c7b70fc50d435.jpg"
SUPPORT_CHAT = "KingVJ01" # Help ke liye username

# --- Messages Script ---
class script(object):
    BROADCAST = "<b>⚡ Status: {}</b>\n\n📢 Total: `{}`\n✅ Success: `{}`\n❌ Failed: `{}`\n⏳ Remaining: `{}`"
    SEARCH_READY = "<b>🏴‍☠️ Your Links is Ready {} 👇\n\n🔐 Any Questions Help @KingVJ01</b>"
    NO_RESULT = "<b>🔻 I Couldn't find anything related to Your Query😕.\n🔺 Did you mean any of these?</b>"
  
