import numpy as np

def pricing_function(days_left, tickets_left, demand_level):
    """
    Optimize ticket pricing to maximize expected revenue.
    
    Args:
        days_left (int): Number of days until the flight
        tickets_left (int): Number of seats remaining
        demand_level (float): Current demand level (known for current day)
    
    Returns:
        float: Optimal ticket price
    """
    if days_left == 0 or tickets_left == 0:
        return 0
    
    # For the current day, we know the exact demand level
    if days_left == 1:
        # On the last day, we want to maximize revenue given current demand
        optimal_price = demand_level / 2
        return min(optimal_price, demand_level - 1)  # Ensure at least 1 ticket can be sold
    
    # For future days, we need to consider the uniform distribution of demand
    # Expected future demand is 150 (average of uniform distribution 100-200)
    #
    # ********* This would be a good place to use a more sophisticated model for future demand *********
    expected_future_demand = 150
    
    # Calculate optimal price considering both current and future demand
    # We use a weighted approach based on days left
    current_weight = 1.0
    future_weight = (days_left - 1) * 0.5  # Future days have less weight
    
    # Optimal price considering both current and future demand
    optimal_price = (
        (current_weight * demand_level + future_weight * expected_future_demand) /
        (current_weight + future_weight)
    ) / 2
    
    # Adjust price based on remaining inventory
    if tickets_left < (demand_level - optimal_price):
        # If we have limited inventory, increase price
        optimal_price = demand_level - tickets_left
    
    # Ensure price is at least 1 and at most demand_level - 1
    optimal_price = max(1, min(optimal_price, demand_level - 1))
    
    return optimal_price

def calculate_expected_revenue(price, demand_level, tickets_left):
    """Calculate expected revenue for a given price and demand level."""
    quantity = min(demand_level - price, tickets_left)
    return price * quantity 