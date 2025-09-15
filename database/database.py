#Codeflix_Botz
#rohit_1888 on Tg

import motor, asyncio
import motor.motor_asyncio
from config import DB_URI, DB_NAME

dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
database = dbclient[DB_NAME]

user_data = database['users']

default_verify = {
    'is_verified': False,
    'verified_time': 0,
    'verify_token': "",
    'link': ""
}

def new_user(id):
    return {
        '_id': id,
        'verify_status': {
            'is_verified': False,
            'verified_time': "",
            'verify_token': "",
            'link': ""
        }
    }

async def present_user(user_id: int):
    found = await user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user = new_user(user_id)
    await user_data.insert_one(user)
    return

async def db_verify_status(user_id):
    user = await user_data.find_one({'_id': user_id})
    if user:
        return user.get('verify_status', default_verify)
    return default_verify

async def db_update_verify_status(user_id, verify):
    await user_data.update_one({'_id': user_id}, {'$set': {'verify_status': verify}})

async def full_userbase():
    user_docs = user_data.find()
    user_ids = [doc['_id'] async for doc in user_docs]
    return user_ids

async def del_user(user_id: int):
    await user_data.delete_one({'_id': user_id})
    return


# --- Premium Expiry ---
async def db_set_premium_expiry(user_id, expires):
    await user_data.update_one({"_id": user_id}, {"$set": {"premium_expires": expires}})

async def db_get_premium_expiry(user_id):
    user = await user_data.find_one({"_id": user_id})
    if user:
        return user.get("premium_expires", 0)
    return 0

# --- Pending Plan ---
async def db_set_pending_plan(user_id, plan):
    await user_data.update_one({"_id": user_id}, {"$set": {"pending_plan": plan}})

async def db_get_pending_plan(user_id):
    user = await user_data.find_one({"_id": user_id})
    if user:
        return user.get("pending_plan", None)
    return None

async def db_clear_pending_plan(user_id):
    await user_data.update_one({"_id": user_id}, {"$unset": {"pending_plan": ""}})


# --- Payment Pending Flag ---
async def db_set_payment_pending(user_id: int, value: bool):
    await user_data.update_one(
        {"_id": user_id},
        {"$set": {"payment_pending": value}},
        upsert=True
    )

async def db_is_payment_pending(user_id: int) -> bool:
    user = await user_data.find_one({"_id": user_id})
    return bool(user and user.get("payment_pending", False))
