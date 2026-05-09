"""Input validation utilities."""

import re
from typing import Union

def validate_domain(domain: str) -> bool:
    """Validate domain name format."""
    if not isinstance(domain, str) or not domain:
        raise ValueError("Domain must be a non-empty string")
        
    # Basic domain validation regex
    pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    
    if not re.match(pattern, domain):
        raise ValueError(f"Invalid domain format: {domain}")
        
    return True
