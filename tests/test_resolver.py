"""Tests for domain resolver functionality."""

import pytest
from unittest.mock import AsyncMock, patch
import sys
import os

# Add src to path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.resolver import DomainResolver, ResolutionResults
from config.config_loader import load_config


@pytest.fixture
def config():
    """Test configuration."""
    return load_config()


class TestDomainResolver:
    """Test cases for DomainResolver class."""
    
    def test_init(self, config):
        """Test resolver initialization."""
        resolver = DomainResolver(config)
        assert resolver.config == config
        
    @pytest.mark.asyncio
    async def test_get_real_ip_valid(self):
        """Test getting real IP for valid domain."""
        resolver = DomainResolver({})
        ip = await resolver.get_real_ip("example.com")
        assert ip is not None
        assert isinstance(ip, str)
        
    @pytest.mark.asyncio
    async def test_get_real_ip_invalid(self):
        """Test getting real IP for invalid domain."""
        resolver = DomainResolver({})
        ip = await resolver.get_real_ip("invalid..domain")
        assert ip is None
        
    @patch('core.services.HackerTargetAPI.fetch_dns_records')
    @pytest.mark.asyncio
    async def test_get_dns_info(self, mock_fetch):
        """Test fetching DNS info."""
        mock_fetch.return_value = "Sample DNS record"
        
        resolver = DomainResolver({})
        result = await resolver.get_dns_info("example.com")
        assert result == "Sample DNS record"
            
    @patch('core.services.HackerTargetAPI.fetch_subdomains')
    @pytest.mark.asyncio
    async def test_get_subdomains(self, mock_fetch):
        """Test fetching subdomains."""
        mock_fetch.return_value = "sub.example.com,192.168.1.1"
        
        resolver = DomainResolver({})
        result = await resolver.get_subdomains("example.com")
        assert result == "sub.example.com,192.168.1.1"
            
    @pytest.mark.asyncio
    async def test_analyze_domain_async(self):
        """Test asynchronous domain analysis."""
        with patch.object(DomainResolver, 'get_real_ip', new=AsyncMock(return_value="93.184.216.34")), \
             patch.object(DomainResolver, 'get_dns_info', new=AsyncMock(return_value="A record")), \
             patch.object(DomainResolver, 'get_subdomains', new=AsyncMock(return_value="www.example.com")):
            
            resolver = DomainResolver({})
            results = await resolver.analyze_domain_async("example.com")
                
            assert isinstance(results, ResolutionResults)
            assert results.real_ip == "93.184.216.34"
            assert results.dns_records == "A record"
            assert results.subdomains == "www.example.com"
