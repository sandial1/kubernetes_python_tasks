def get_total(costs: dict[str, float], items: list[str], tax: float) -> float:
    """
    Calculate the total cost of items plus tax rounded to two decimal places.

    Args:
        costs: Dictionary mapping item names to their costs
        items: List of items to purchase (may contain duplicates)
        tax: Tax rate as a decimal (e.g., 0.09 for 9%)

    Returns:
        Total cost including tax, rounded to 2 decimal places

    Example:
        >>> costs = {"socks": 5, "shoes": 60, "sweater": 30}
        >>> get_total(costs, ["socks", "shoes"], 0.09)
        70.85
    """
    subtotal = sum(costs.get(item, 0) for item in items)

    tax_amount = subtotal * tax

    total = subtotal + tax_amount

    return round(total, 2)
