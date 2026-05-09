"""External service integrations."""

from typing import Optional
import aiohttp
import sys
import os

# Add src to path for relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import get_logger

logger = get_logger(__name__)

class HackerTargetAPI:
    """HackerTarget API client."""
    
    BASE_URL = "https://api.hackertarget.com"
    
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        
    async def fetch_dns_records(self, domain: str) -> Optional[str]:
        """Fetch DNS records from HackerTarget."""
        url = f"{self.BASE_URL}/dnslookup/?q={domain}"
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                    logger.debug(f"Fetched DNS records for {domain}")
                    content = text.strip()
                    return content if content and content != "error" else None
                else:
                    logger.warning(f"HackerTarget returned status {response.status} for DNS lookup")
                    return None
        except Exception as e:
            logger.error(f"DNS record fetch failed: {e}")
            return None
            
    async def fetch_subdomains(self, domain: str) -> Optional[str]:
        """Fetch subdomains from HackerTarget."""
        url = f"{self.BASE_URL}/hostsearch/?q={domain}"
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                    logger.debug(f"Fetched subdomains for {domain}")
                    content = text.strip()
                    return content if content and content != "error" else None
                else:
                    logger.warning(f"HackerTarget returned status {response.status} for subdomain search")
                    return None
        except Exception as e:
            logger.error(f"Subdomain fetch failed: {e}")
            return None
