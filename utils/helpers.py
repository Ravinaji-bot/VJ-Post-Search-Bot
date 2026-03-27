# Updated utils/helpers.py
# Don't Remove Credit Tg - @VJ_Botz

import motor.motor_asyncio
from info import DATABASE_URI, DATABASE_NAME
import asyncio

# MongoDB Connection
client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]
user_data = db.users
group_data = db.groups

async def add_user(user_id):
    if not await user_data.find_one({'_id': user_id}):
        await user_data.insert_one({'_id': user_id})

async def get_users():
    users = user_data.find({})
    count = await user_data.count_documents({})
    return count, users

async def delete_user(user_id):
    await user_data.delete_one({'_id': user_id})

async def add_channel(group_id, channel_id):
    group = await group_data.find_one({'_id': group_id})
    if group:
        channels = group.get('channels', [])
        if channel_id not in channels:
            channels.append(channel_id)
            await group_data.update_one({'_id': group_id}, {'$set': {'channels': channels}})
            return True
        return False
    else:
        await group_data.insert_one({'_id': group_id, 'channels': [channel_id]})
        return True

async def get_group(group_id):
    group = await group_data.find_one({'_id': group_id})
    return group if group else {"channels": []}

async def remove_group(group_id):
    await group_data.delete_one({'_id': group_id})
    return True

async def get_groups():
    groups = group_data.find({})
    count = await group_data.count_documents({})
    return count, groups
    
