import asyncio
from fastmcp import Client

"""
client = Client("my_server.py")

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(f"Result: {result}")

asyncio.run(call_tool("Ford"))
"""

client = Client("server.py")

"""async def call_users():
    async with client:
        result = await client.call_tool("search_users", {})
        print(f"Result: {result}")

asyncio.run(call_users())"""

async def call_get_user_by_id(user_id: str):
    async with client:
        result = await client.call_tool("get_user_by_id", {"user_id": user_id})
        print(f"Result: {result}")  

asyncio.run(call_get_user_by_id("ocid1.user.oc1..aaaaaaaapdr7ehohhhvlplzhwp4xuu2et526gy3zjz62pofgpqalebefwb2q"))
