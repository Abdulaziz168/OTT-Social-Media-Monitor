"""Test analytics calculator."""

import pytest
from instagram_monitor.analytics import AnalyticsCalculator


class TestAnalyticsCalculator:
    """Test analytics calculator."""

    def test_calculate_engagement_rate(self):
        """Test engagement rate calculation."""
        calc = AnalyticsCalculator(None)
        
        # Test case: 100 likes, 10 comments, 1000 followers
        # Engagement rate = (100 + 10) / 1000 * 100 = 11%
        rate = calc.calculate_engagement_rate(100, 10, 1000)
        assert rate == 11.0

    def test_calculate_engagement_rate_zero_followers(self):
        """Test engagement rate with zero followers."""
        calc = AnalyticsCalculator(None)
        
        rate = calc.calculate_engagement_rate(100, 10, 0)
        assert rate == 0.0

    def test_calculate_growth_rate(self):
        """Test growth rate calculation."""
        calc = AnalyticsCalculator(None)
        
        # Test case: current 1100, previous 1000
        # Growth rate = (1100 - 1000) / 1000 * 100 = 10%
        rate = calc.calculate_growth_rate(1100, 1000)
        assert rate == 10.0

    def test_calculate_growth_rate_zero_previous(self):
        """Test growth rate with zero previous value."""
        calc = AnalyticsCalculator(None)
        
        rate = calc.calculate_growth_rate(1000, 0)
        assert rate == 0.0
