"""OCI IAM Domain MCP Server.

This module is FastMCP server implementation for interacting with OCI IAM Domains.
"""

import logging
from fastmcp import FastMCP, Context
from typing import Dict, List
from starlette.requests import Request
from starlette.responses import PlainTextResponse
import oci
from config.config_manager import ConfigManager
from utils.oci_client_manager import OCIClientManager
from utils.oci_utility import OCIUtility
from resources import users
import asyncio

#Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Creating MCP Server
mcp = FastMCP("OCI IAM Domain MCP Server")

oci_config_manager = ConfigManager()
oci_client_manager = OCIClientManager(oci_config_manager)

@mcp.tool()
async def search_users(ctx: Context) -> List[Dict[str, str]]:
    """Search for all users in the Identity Domain
    
    Args: 
        ctx: FastMCP context object
    
    Returns: 
        A dictionary containing user details.
        
    """
    try:
        identity_domains_client = oci_client_manager.get_iam_domain_client()
        logger.info(f"Searching users in Identity Domain: {oci_config_manager.get_domain_guid()}")
        AuthzCode = OCIUtility.get_authorization_token(oci_config_manager.get_client_id(), oci_config_manager.get_client_secret())
        formatted_users = await users.search_users(identity_domains_client, AuthzCode, "", 100)
        logger.info(f"Formatted Users from search users: {formatted_users}")
        await ctx.report_progress(progress=100, total=100)
        return formatted_users
    except Exception as e:
        logger.error(f"Error searching users: {e}")
        return []

@mcp.tool()
async def get_user_by_id(ctx: Context, user_id: str) -> Dict[str, str]:
    """Get a user by ID from the Identity Domain

    Args:
        ctx: FastMCP context object
        user_id: The ID of the user to retrieve

    Returns:
        A dictionary containing user details.
    """
    try:
        identity_domains_client = oci_client_manager.get_iam_domain_client()
        logger.info(f"Getting user by ID in Identity Domain: {oci_config_manager.get_domain_guid()}")
        AuthzCode = OCIUtility.get_authorization_token(oci_config_manager.get_client_id(), oci_config_manager.get_client_secret())
        user = await users.get_user_by_id(identity_domains_client, AuthzCode, user_id)
        logger.info(f"Formatted User from get user by ID: {user}")
        await ctx.report_progress(progress=100, total=100)
        return user
    except Exception as e:
        logger.error(f"Error getting user by ID: {e}")
        return {}

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a Welcome greeting"""
    return f"Welcome, {name}!"

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

