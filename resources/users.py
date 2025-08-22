import oci
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def search_users(identity_domains_client, authzCode: str, query: str, limit: int) -> List[Dict[str,str]]:
    try:
        logger.info(f"Searching users with query: {query} and limit: {limit}")
        search_users_response = identity_domains_client.search_users(
            authorization=authzCode,
            user_search_request=oci.identity_domains.models.UserSearchRequest(
                schemas=["urn:ietf:params:scim:api:messages:2.0:SearchRequest"]
            )
        )
        logger.info(f"Search Users Response: {search_users_response.data}")
        formatted_users = []
        user_resources = search_users_response.data.resources
        for user in user_resources:
            formatted_users.append({
                "id": user.id,
                "name": user.user_name,
                "first_name": user.name.given_name if user.name else "firstName",
                "last_name": user.name.family_name if user.name else "familyName",
                "email": user.emails[0].value if user.emails else "email",
                "display_name": user.display_name if user.display_name else "displayName"
            })
        logger.info(f"Formatted Users: {formatted_users}")
        return formatted_users
    except Exception as e:
        logger.error(f"Error searching users: {e}")
        return []

async def get_user_by_id(identity_domains_client, authzCode: str, user_id: str) -> Dict[str, str]:
    try:
        logger.info(f"Getting user by ID: {user_id}")
        get_user_response = identity_domains_client.get_user(
            authorization=authzCode,
            user_id=user_id
        )
        logger.info(f"Get User Response: {get_user_response.data}")
        return {
            "id": get_user_response.data.id,
            "name": get_user_response.data.user_name,
            "first_name": get_user_response.data.name.given_name if get_user_response.data.name else "firstName",
            "last_name": get_user_response.data.name.family_name if get_user_response.data.name else "familyName",
            "email": get_user_response.data.emails[0].value if get_user_response.data.emails else "email",
            "display_name": get_user_response.data.display_name if get_user_response.data.display_name else "displayName"
        }
    except Exception as e:
        logger.error(f"Error getting user by ID: {e}")
        return {}

async def search_user_by_name(identity_domains_client, authzCode: str, user_name: str) -> List[Dict[str, str]]:
    try:
        logger.info(f"Getting user by name: {user_name}")
        filter = f'userName co \"{user_name}\" or emails.value co \"{user_name}\" or displayName co \"{user_name}\"'
        logger.info(f"Filter for search: {filter}")
        search_users_response = identity_domains_client.search_users(
            authorization=authzCode,
            user_search_request=oci.identity_domains.models.UserSearchRequest(
                schemas=["urn:ietf:params:scim:api:messages:2.0:SearchRequest"],
                filter=filter
            )
        )
        #logger.info(f"Search Users Response: {search_users_response.data}")
        formatted_users = []
        user_resources = search_users_response.data.resources
        for user in user_resources:
            formatted_users.append({
                "id": user.id,
                "name": user.user_name,
                "first_name": user.name.given_name if user.name else "firstName",
                "last_name": user.name.family_name if user.name else "familyName",
                "email": user.emails[0].value if user.emails else "email",
                "display_name": user.display_name if user.display_name else "displayName"
            })
        #logger.info(f"Formatted Users: {formatted_users}")
        return formatted_users
    except Exception as e:
        logger.error(f"Error searching users: {e}")
        return []

async def create_user(identity_domains_client, authzCode: str, user_data: Dict[str, str]) -> Dict[str, str]:
    try:
        logger.info(f"Creating user with data: {user_data}")
        create_user_response = identity_domains_client.create_user(
            authorization=authzCode,
            user_create_request=oci.identity_domains.models.User(
                schemas=["urn:ietf:params:scim:api:messages:2.0:CreateRequest"],
                userName=user_data.get("name"),
                name=oci.identity_domains.models.UserName(
                    given_name=user_data.get("first_name"),
                    family_name=user_data.get("last_name")
                ),
                emails=[
                    oci.identity_domains.models.UserEmails(
                        value=user_data.get("email"),
                        type="work"
                    )
                ],
                display_name=user_data.get("display_name")
            )
        )
        logger.info(f"Create User Response: {create_user_response.data}")
        return {
            "id": create_user_response.data.id,
            "name": create_user_response.data.user_name,
            "first_name": create_user_response.data.name.given_name if create_user_response.data.name else "firstName",
            "last_name": create_user_response.data.name.family_name if create_user_response.data.name else "familyName",
            "email": create_user_response.data.emails[0].value if create_user_response.data.emails else "email",
            "display_name": create_user_response.data.display_name if create_user_response.data.display_name else "displayName"
        }
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return {}