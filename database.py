import motor.motor_asyncio as ma
from model import Member
from bson.objectid import ObjectId

client = ma.AsyncIOMotorClient("mongodb://localhost:27017/")
database = client.rami_db
collection = database.member


# ------------------------

async def fetch_one_member(member_id):
    _id = ObjectId(member_id)
    document = await collection.find_one({"_id": _id})
    return document

async def fetch_all_members():
    members = []
    cursor = collection.find({})
    async for document in cursor:
        members.append(Member(**document))
    return members

async def create_member(member):
    document = member
    result = await collection.insert_one(document)
    return document


async def update_member_name(member_id, name):
    _id = ObjectId(member_id)
    document = await collection.find_one({"_id": _id})
    await document.update_one({"$set": {"name": name}})
    return document

async def remove_member(name):
    await collection.delete_one({"name": name})
    return True

# ------------------------