"""Tests for CLI interface."""

import pytest
from unittest.mock import patch
import sys
from io import StringIO
import os

# Add src to path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cli import main, run_analysis


class TestCLI:
    """Test cases for CLI interface."""
    
    @patch('cli.DomainResolver')
    def test_run_analysis_success(self, mock_resolver):
        """Test successful domain analysis."""
        # Mock the resolver results
        from core.resolver import ResolutionResults
        mock_results = ResolutionResults(
            real_ip="93.184.216.34",
            dns_records="A record",
            subdomains="www.example.com"
        )
        
        mock_instance = mock_resolver.return_value
        mock_instance.analyze_domain.return_value = mock_results
        
        # Capture stdout
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        
        result = run_analysis("example.com")
        
        # Restore stdout
        sys.stdout = old_stdout
        
        assert result == 0
        output = captured_output.getvalue()
        assert "93.184.216.34" in output
        assert "A record" in output
        assert "www.example.com" in output
        
    @patch('cli.DomainResolver')
    def test_run_analysis_failure(self, mock_resolver):
        """Test domain analysis failure."""
        # Mock resolver to raise exception
        mock_instance = mock_resolver.return_value
        mock_instance.analyze_domain.side_effect = Exception("Test error")
        
        # Capture stderr
        captured_error = StringIO()
        old_stderr = sys.stderr
        sys.stderr = captured_error
        
        result = run_analysis("example.com")
        
        # Restore stderr
        sys.stderr = old_stderr
        
        assert result == 1
