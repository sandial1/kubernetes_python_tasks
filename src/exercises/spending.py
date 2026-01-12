def get_total(costs: dict[str, float], items: list[str], tax: float) -> float:
    """
    Calculate the total cost of items plus tax.

    Given a dictionary of items and their costs, an array specifying items bought,
    and a tax rate, calculate the total cost of the items plus the given tax.

    If an item doesn't exist in the given cost values, the item is ignored.
    Output should be rounded to two decimal places.

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
    # Calculate subtotal by summing costs of valid items
    subtotal = sum(costs.get(item, 0) for item in items)

    # Calculate tax amount
    tax_amount = subtotal * tax

    # Calculate total and round to 2 decimal places
    total = subtotal + tax_amount

    return round(total, 2)
