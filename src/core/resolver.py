"""Domain resolution core logic."""

import asyncio
import socket
from dataclasses import dataclass
from typing import Optional, Dict, Any
import sys
import os

# Add src to path for relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import aiohttp
from utils.logger import get_logger
from utils.validators import validate_domain
from core.services import HackerTargetAPI

logger = get_logger(__name__)

@dataclass
class ResolutionResults:
    """Container for resolution results."""
    real_ip: Optional[str] = None
    dns_records: Optional[str] = None
    subdomains: Optional[str] = None

class DomainResolver:
    """Handles domain resolution tasks."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def get_real_ip(self, domain: str) -> Optional[str]:
        """Resolve domain to real IP address."""
        try:
            validate_domain(domain)
            loop = asyncio.get_event_loop()
            ip = await loop.run_in_executor(None, socket.gethostbyname, domain)
            logger.info(f"Resolved {domain} to IP: {ip}")
            return ip
        except Exception as e:
            logger.error(f"Failed to resolve IP for {domain}: {e}")
            return None
            
    async def get_dns_info(self, domain: str) -> Optional[str]:
        """Fetch DNS records for domain."""
        try:
            validate_domain(domain)
            timeout = aiohttp.ClientTimeout(total=self.config.get('timeout', 30))
            async with aiohttp.ClientSession(timeout=timeout) as session:
                api = HackerTargetAPI(session)
                return await api.fetch_dns_records(domain)
        except Exception as e:
            logger.error(f"Failed to fetch DNS info for {domain}: {e}")
            return None
            
    async def get_subdomains(self, domain: str) -> Optional[str]:
        """Find subdomains for domain."""
        try:
            validate_domain(domain)
            timeout = aiohttp.ClientTimeout(total=self.config.get('timeout', 30))
            async with aiohttp.ClientSession(timeout=timeout) as session:
                api = HackerTargetAPI(session)
                return await api.fetch_subdomains(domain)
        except Exception as e:
            logger.error(f"Failed to fetch subdomains for {domain}: {e}")
            return None
            
    async def analyze_domain_async(self, domain: str) -> ResolutionResults:
        """Asynchronously analyze domain."""
        logger.info(f"Starting analysis for domain: {domain}")
        
        # Run all tasks concurrently
        tasks = [
            self.get_real_ip(domain),
            self.get_dns_info(domain),
            self.get_subdomains(domain)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions in results
        real_ip = results[0] if not isinstance(results[0], Exception) else None
        dns_records = results[1] if not isinstance(results[1], Exception) else None
        subdomains = results[2] if not isinstance(results[2], Exception) else None
        
        return ResolutionResults(
            real_ip=real_ip,
            dns_records=dns_records,
            subdomains=subdomains
        )
        
    def analyze_domain(self, domain: str) -> ResolutionResults:
        """Analyze domain synchronously."""
        try:
            return asyncio.run(self.analyze_domain_async(domain))
        except Exception as e:
            logger.error(f"Domain analysis failed: {e}")
            return ResolutionResults()
