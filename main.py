from fastapi import FastAPI, HTTPException

from model import Member

from database import (
    fetch_one_member,
    fetch_all_members,
    create_member,
    update_member_name,
    remove_member
)

# an HTTP-specific exception class  to generate exception information

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# ------------------------

@app.get("/api/members/")
async def get_members():
    response = await fetch_all_members()
    return response

@app.get("/api/members/{id}", response_model=Member)
async def get_member_by_id(id):
    response = await fetch_one_member(id)
    if response:
        return response
    raise HTTPException(404, f"There is no member")

@app.post("/api/members/", response_model=Member)
async def post_member(member: Member):
    response = await create_member(member.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@app.put("/api/members/{id}/", response_model=Member)
async def put_member(id: str, name: str):
    response = await update_member_name(id, name)
    if response:
        return response
    raise HTTPException(404, f"There is no member ")

@app.delete("/api/members/{id}")
async def delete_member(id):
    response = await remove_member(id)
    if response:
        return "Successfully deleted member"
    raise HTTPException(404, f"There is no member ")

# ------------------------
