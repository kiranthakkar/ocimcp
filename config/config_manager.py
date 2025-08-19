import oci
import configparser
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigManager:
    
    def __init__(self):
        domain_guid = None
        oci_config = None
        client_id = None
        client_secret = None
        
        env_paths = [
            #Config Directory form project root
            Path(__file__).parent / "config.ini",
            #Current working directory config
            Path.cwd() / "config.ini",
            #User's home directory
            Path.home() / ".oci" / "mcp" / "config.ini"
        ]
        for env_path in env_paths:
            if env_path.exists():
                self.load_config(env_path)
                logger.info(f"Loaded environment configuration from {env_path}")
            else:
                logger.warning(f"Environment configuration not found at {env_path}")

    def load_config(self, file_path: str):
        config = configparser.ConfigParser()
        try:
            config.read(file_path)

            self.domain_guid = config.get('IAMDOMAIN', 'domain_guid', fallback=None)
            self.client_id = config.get('IAMDOMAIN', 'client_id', fallback=None)
            self.client_secret = config.get('IAMDOMAIN', 'client_secret', fallback=None)
            self.oci_config = oci.config.from_file(file_path, "OCI")
        except Exception as e:
            logger.error(f"Error loading config from {file_path}: {e}")

    def get_oci_config(self):
        return self.oci_config

    def get_domain_guid(self):
        return self.domain_guid

    def get_client_id(self):
        return self.client_id

    def get_client_secret(self):
        return self.client_secret