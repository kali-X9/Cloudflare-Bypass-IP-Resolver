"""System health checking functionality."""

import sys
import os
from typing import Dict, Any
import asyncio
import aiohttp

# Add src to path for relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import get_logger
from config.config_loader import load_config

logger = get_logger(__name__)

def check_dependencies() -> Dict[str, bool]:
    """Check if required dependencies are available."""
    checks = {}
    
    # Check standard library modules
    checks['socket'] = True  # Always available
    
    # Check third-party libraries
    try:
        import requests
        checks['requests'] = True
    except ImportError:
        checks['requests'] = False
        
    try:
        import yaml
        checks['pyyaml'] = True
    except ImportError:
        checks['pyyaml'] = False
        
    try:
        import aiohttp
        checks['aiohttp'] = True
    except ImportError:
        checks['aiohttp'] = False
        
    return checks

async def check_api_connectivity() -> bool:
    """Check connectivity to external APIs."""
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get("https://api.hackertarget.com/dnslookup/?q=example.com") as response:
                return response.status == 200
    except Exception:
        return False

def perform_health_check() -> int:
    """Perform comprehensive health check."""
    print("[+] Performing system health check...")
    
    # Load configuration
    try:
        config = load_config()
        print("[+] Configuration loaded successfully")
    except Exception as e:
        print(f"[-] Configuration error: {e}")
        return 1
        
    # Check dependencies
    deps = check_dependencies()
    all_deps_ok = all(deps.values())
    
    print("[+] Dependency check:")
    for dep, status in deps.items():
        status_str = "OK" if status else "MISSING"
        print(f"  {dep}: {status_str}")
        
    if not all_deps_ok:
        print("[-] Some dependencies are missing")
        return 1
        
    # Check API connectivity
    try:
        api_ok = asyncio.run(check_api_connectivity())
        print(f"[+] External API connectivity: {'OK' if api_ok else 'FAILED'}")
        
        if not api_ok:
            print("[-] Cannot connect to external APIs")
            return 1
    except Exception as e:
        print(f"[-] API connectivity check failed: {e}")
        return 1
        
    print("[+] All health checks passed")
    return 0
