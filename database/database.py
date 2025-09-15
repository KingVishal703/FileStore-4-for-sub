# Codeflix_Botz
# rohit_1888 on Tg

import motor.motor_asyncio
from config import DB_URI, DB_NAME

# MongoDB client setup
dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
database = dbclient[DB_NAME]

# Users collection
user_data = database['users']

# Default verification structure
default_verify = {
    "is_verified": False,
    "verified_time": 0,
    "verify_token": "",
    "link": ""
}

# New user template
def new_user(user_id: int):
    return {
        "_id": user_id,
        "verify_status": default_verify.copy(),
        "premium_expires": 0,
        "pending_plan": None,
        "payment_pending": False,
    }

# --- User Management ---
async def present_user(user_id: int) -> bool:
    user = await user_data.find_one({"_id": user_id})
    return bool(user)

async def add_user(user_id: int):
    user = new_user(user_id)
    await user_data.update_one({"_id": user_id}, {"$setOnInsert": user}, upsert=True)

async def del_user(user_id: int):
    await user_data.delete_one({"_id": user_id})

async def full_userbase():
    user_docs = user_data.find()
    return [doc["_id"] async for doc in user_docs]

# --- Verification ---
async def db_verify_status(user_id: int) -> dict:
    user = await user_data.find_one({"_id": user_id})
    if user and "verify_status" in user:
        return user["verify_status"]
    return default_verify.copy()

async def db_update_verify_status(user_id: int, verify: dict):
    await user_data.update_one(
        {"_id": user_id},
        {"$set": {"verify_status": verify}},
        upsert=True
    )

# --- Premium Expiry ---
async def db_set_premium_expiry(user_id: int, expires: int):
    await user_data.update_one(
        {"_id": user_id},
        {"$set": {"premium_expires": expires}},
        upsert=True
    )

async def db_get_premium_expiry(user_id: int) -> int:
    user = await user_data.find_one({"_id": user_id})
    return user.get("premium_expires", 0) if user else 0

# --- Pending Plan ---
async def db_set_pending_plan(user_id: int, plan: str):
    await user_data.update_one(
        {"_id": user_id},
        {"$set": {"pending_plan": plan}},
        upsert=True
    )

async def db_get_pending_plan(user_id: int):
    user = await user_data.find_one({"_id": user_id})
    return user.get("pending_plan", None) if user else None

async def db_clear_pending_plan(user_id: int):
    await user_data.update_one(
        {"_id": user_id},
        {"$unset": {"pending_plan": ""}}
    )

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
