import oci
from config.config_manager import ConfigManager
import base64
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCIClientManager:
    configManager = None
    iam_domain_client = None
    iam_client = None

    def __init__(self, configManager = None):
        if configManager is None:
            configManager = ConfigManager()
        self.iam_domain_client = oci.identity_domains.IdentityDomainsClient(configManager.get_oci_config(),configManager.get_domain_guid(),)
        self.iam_client = oci.identity.IdentityClient(configManager.get_oci_config())

    def get_iam_domain_client(self):
        return self.iam_domain_client

    def get_iam_client(self):
        return self.iam_client

    def get_config_manager(self):
        return self.configManager