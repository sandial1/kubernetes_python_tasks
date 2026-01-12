import pytest
from exercises.spending import get_total


class TestBasicCalculations:
    """Test basic cost calculations."""
    
    def test_example_from_kata(self):
        """Test the exact example from the kata description."""
        costs = {"socks": 5, "shoes": 60, "sweater": 30}
        result = get_total(costs, ["socks", "shoes"], 0.09)
        assert result == 70.85
    
    def test_single_item(self):
        """Should calculate correctly with a single item."""
        costs = {"apple": 2.00}
        result = get_total(costs, ["apple"], 0.10)
        # 2.00 + (2.00 * 0.10) = 2.20
        assert result == 2.20
    
    def test_multiple_items_no_duplicates(self):
        """Should sum multiple different items."""
        costs = {"bread": 3.50, "milk": 4.00, "eggs": 2.50}
        result = get_total(costs, ["bread", "milk", "eggs"], 0.05)
        # (3.50 + 4.00 + 2.50) * 1.05 = 10.50
        assert result == 10.50
    
    def test_duplicate_items(self):
        """Should count the same item multiple times."""
        costs = {"cookie": 1.50}
        result = get_total(costs, ["cookie", "cookie", "cookie"], 0.08)
        # (1.50 * 3) * 1.08 = 4.86
        assert result == 4.86


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_empty_items_list(self):
        """Should return 0.00 when no items are purchased."""
        costs = {"item": 10.00}
        result = get_total(costs, [], 0.10)
        assert result == 0.00
    
    def test_zero_tax(self):
        """Should handle 0% tax correctly."""
        costs = {"item": 10.00}
        result = get_total(costs, ["item"], 0.00)
        assert result == 10.00
    
    def test_high_tax_rate(self):
        """Should handle high tax rates correctly."""
        costs = {"luxury": 100.00}
        result = get_total(costs, ["luxury"], 0.25)
        # 100 + (100 * 0.25) = 125.00
        assert result == 125.00
    
    def test_fractional_costs(self):
        """Should handle items with decimal costs."""
        costs = {"pen": 0.99, "paper": 2.49}
        result = get_total(costs, ["pen", "paper"], 0.07)
        # (0.99 + 2.49) * 1.07 = 3.7236 -> 3.72
        assert result == 3.72
    
    def test_very_small_amounts(self):
        """Should handle very small amounts correctly."""
        costs = {"candy": 0.05}
        result = get_total(costs, ["candy"], 0.06)
        # 0.05 * 1.06 = 0.053 -> 0.05
        assert result == 0.05


class TestInvalidItems:
    """Test handling of items not in the costs dictionary."""
    
    def test_nonexistent_item_ignored(self):
        """Should ignore items not in the costs dictionary."""
        costs = {"apple": 1.00, "banana": 0.50}
        result = get_total(costs, ["apple", "orange"], 0.10)
        # Only apple is counted: 1.00 * 1.10 = 1.10
        assert result == 1.10
    
    def test_all_items_nonexistent(self):
        """Should return 0.00 when all items are invalid."""
        costs = {"apple": 1.00}
        result = get_total(costs, ["orange", "grape"], 0.10)
        assert result == 0.00
    
    def test_mix_valid_and_invalid_items(self):
        """Should only count valid items in calculation."""
        costs = {"a": 10.00, "b": 20.00}
        result = get_total(costs, ["a", "x", "b", "y", "a"], 0.10)
        # a + b + a = 10 + 20 + 10 = 40, with tax: 44.00
        assert result == 44.00


class TestRounding:
    """Test proper rounding to 2 decimal places."""
    
    def test_rounds_down(self):
        """Should round down when third decimal is < 5."""
        costs = {"item": 10.00}
        result = get_total(costs, ["item"], 0.011)
        # 10.00 * 1.011 = 10.11 (exact)
        assert result == 10.11
    
    def test_rounds_up(self):
        """Should round up when third decimal is >= 5."""
        costs = {"item": 10.00}
        result = get_total(costs, ["item"], 0.016)
        # 10.00 * 1.016 = 10.16 (exact)
        assert result == 10.16
    
    def test_complex_rounding_scenario(self):
        """Should handle complex rounding correctly."""
        costs = {"item": 33.33}
        result = get_total(costs, ["item"], 0.0666)
        # 33.33 * 1.0666 = 35.5497778 -> 35.55
        assert result == 35.55


class TestRealWorldScenarios:
    """Test realistic shopping scenarios."""
    
    def test_grocery_shopping(self):
        """Test a realistic grocery shopping trip."""
        costs = {
            "milk": 3.99,
            "bread": 2.50,
            "eggs": 4.25,
            "cheese": 5.99,
            "butter": 4.50
        }
        items = ["milk", "bread", "eggs", "eggs", "cheese"]
        result = get_total(costs, items, 0.08)
        # 3.99 + 2.50 + 4.25 + 4.25 + 5.99 = 20.98
        # 20.98 * 1.08 = 22.6584 -> 22.66
        assert result == 22.66
    
    def test_clothing_store(self):
        """Test buying multiple clothes items with high tax."""
        costs = {
            "shirt": 29.99,
            "pants": 49.99,
            "socks": 9.99,
            "jacket": 89.99
        }
        items = ["shirt", "pants", "socks", "socks"]
        result = get_total(costs, items, 0.0825)
        # 29.99 + 49.99 + 9.99 + 9.99 = 99.96
        # 99.96 * 1.0825 = 108.2097 -> 108.21
        assert result == 108.21
    
    def test_empty_costs_dictionary(self):
        """Should handle empty costs dictionary."""
        result = get_total({}, ["anything"], 0.10)
        assert result == 0.00