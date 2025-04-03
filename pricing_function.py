import numpy as np

def pricing_function(days_left, tickets_left, demand_level):
    """
    Optimize ticket pricing to maximize expected revenue with dynamic seat-based pricing.
    Adjusted for business class pricing with higher price points and lower demand levels.
    
    Args:
        days_left (int): Number of days until the flight
        tickets_left (int): Number of seats remaining
        demand_level (float): Current demand level (known for current day)
    
    Returns:
        float: Optimal ticket price
    """
    if tickets_left <= 0:  # Only return 0 if no tickets left
        return 0
    
    # Base price calculation (adjusted for business class scale)
    base_price = 900  # Starting base price for business class
    
    # Demand factor (adjusted for actual demand numbers from data)
    demand_factor = 1 + max(0, (demand_level - 25) / 25)
    
    # Inventory pressure factor
    total_seats = 50  # Assuming business class has fewer seats
    inventory_factor = 1 + max(0, (1 - tickets_left/total_seats)) * 0.3
    
    # Time pressure factor
    time_factor = 1 + max(0, (1 - days_left/30)) * 0.2
    
    # Calculate optimal price
    optimal_price = base_price * demand_factor * inventory_factor * time_factor
    
    # Adjust price based on demand level
    if demand_level > 30:
        optimal_price *= 1.1  # 10% premium for high demand
    elif demand_level < 20:
        optimal_price *= 0.95  # 5% discount for low demand
    
    # Last minute pricing
    if days_left <= 3:
        if tickets_left > 20:  # Many seats left
            optimal_price *= 0.9  # 10% discount
        else:
            optimal_price *= 1.1  # 10% premium
    
    # Ensure price stays within reasonable bounds for business class
    optimal_price = max(800, min(optimal_price, 1200))
    
    return optimal_price

def calculate_expected_revenue(price, demand_level, tickets_left):
    """
    Calculate expected revenue for a given price and demand level.
    For business class, assume demand is less elastic (less sensitive to price).
    """
    # Calculate actual demand based on price elasticity
    price_elasticity = 0.5  # Business class is less elastic
    actual_demand = demand_level * (1 - price_elasticity * (price - 900) / 900)
    actual_demand = max(0, min(actual_demand, demand_level))
    
    # Calculate quantity sold
    quantity = min(actual_demand, tickets_left)
    return price * quantity 