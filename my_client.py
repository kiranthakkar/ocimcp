import asyncio
from fastmcp import Client

client = Client("server.py")

async def call_users():
    async with client:
        search_result = await client.call_tool("search_users", {})
        print(f"Search users Result: {search_result}")
        get_result = await client.call_tool("get_user_by_id", {"user_id": "ocid1.user.oc1..aaaaaaaapdr7ehohhhvlplzhwp4xuu2et526gy3zjz62pofgpqalebefwb2q"})
        print(f"Get User Result: {get_result}")
asyncio.run(call_users())