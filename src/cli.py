"""Command-line interface for the Cloudflare bypass tool."""

import argparse
import sys
import os
from typing import Optional

# Add src to path for relative imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.resolver import DomainResolver
from health.checker import perform_health_check
from utils.logger import get_logger
from config.config_loader import load_config

logger = get_logger(__name__)

def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description="Cloudflare Bypass & IP Resolver",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -d example.com
  %(prog)s -d example.com --config custom.yaml
        """
    )
    
    parser.add_argument(
        "-d", "--domain",
        type=str,
        required=True,
        help="Target domain to analyze"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--health",
        action="store_true",
        help="Perform health check"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s {version}".format(version="1.0.0")
    )
    
    return parser

def run_analysis(domain: str, config_path: Optional[str] = None) -> int:
    """Run domain analysis."""
    try:
        config = load_config(config_path)
        
        resolver = DomainResolver(config)
        results = resolver.analyze_domain(domain)
        
        # Output results
        print(f"\n[+] Analysis Results for {domain}:")
        print("=" * 50)
        
        if results.real_ip:
            print(f"[+] Real IP Address: {results.real_ip}")
        else:
            print("[-] Could not resolve real IP address")
            
        if results.dns_records:
            print("\n[+] DNS Records:")
            print(results.dns_records)
        else:
            print("\n[-] No DNS records found")
            
        if results.subdomains:
            print("\n[+] Subdomains:")
            print(results.subdomains)
        else:
            print("\n[-] No subdomains found")
            
        return 0
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return 1

def main() -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if args.health:
        return perform_health_check()
    
    return run_analysis(args.domain, args.config)

if __name__ == "__main__":
    sys.exit(main())
