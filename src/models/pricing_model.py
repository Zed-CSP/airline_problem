"""
Pricing model implementation for airline ticket pricing optimization.
"""

from typing import Tuple


class BusinessClassPricingModel:
    """Pricing model for business class airline tickets."""
    
    def __init__(self, 
                 base_price: float = 900,
                 min_price: float = 800,
                 max_price: float = 1200,
                 price_elasticity: float = 0.5):
        """
        Initialize the pricing model.
        
        Args:
            base_price: Base price for business class tickets
            min_price: Minimum allowed price
            max_price: Maximum allowed price
            price_elasticity: Price elasticity of demand (0-1)
        """
        self.base_price = base_price
        self.min_price = min_price
        self.max_price = max_price
        self.price_elasticity = price_elasticity
    
    def calculate_price(self, 
                       days_left: int, 
                       tickets_left: int, 
                       demand_level: float) -> float:
        """
        Calculate optimal ticket price based on current conditions.
        
        Args:
            days_left: Number of days until flight
            tickets_left: Number of seats remaining
            demand_level: Current demand level
            
        Returns:
            float: Optimal ticket price
        """
        if tickets_left <= 0:
            return 0
        
        # Calculate demand factor
        demand_factor = 1 + max(0, (demand_level - 25) / 25)
        
        # Calculate inventory factor
        total_seats = 50  # Business class capacity
        inventory_factor = 1 + max(0, (1 - tickets_left/total_seats)) * 0.3
        
        # Calculate time factor
        time_factor = 1 + max(0, (1 - days_left/30)) * 0.2
        
        # Calculate optimal price
        optimal_price = self.base_price * demand_factor * inventory_factor * time_factor
        
        # Apply demand-based adjustments
        if demand_level > 30:
            optimal_price *= 1.1  # High demand premium
        elif demand_level < 20:
            optimal_price *= 0.95  # Low demand discount
        
        # Apply last-minute pricing
        if days_left <= 3:
            if tickets_left > 20:
                optimal_price *= 0.9  # Last-minute discount
            else:
                optimal_price *= 1.1  # Last-minute premium
        
        # Ensure price stays within bounds
        return max(self.min_price, min(optimal_price, self.max_price))
    
    def calculate_revenue(self, 
                         price: float, 
                         demand_level: float, 
                         tickets_left: int) -> Tuple[float, float]:
        """
        Calculate expected revenue and quantity sold for given price and demand.
        
        Args:
            price: Ticket price
            demand_level: Current demand level
            tickets_left: Number of seats remaining
            
        Returns:
            Tuple[float, float]: (revenue, quantity_sold)
        """
        # Calculate actual demand based on price elasticity
        actual_demand = demand_level * (1 - self.price_elasticity * (price - self.base_price) / self.base_price)
        actual_demand = max(0, min(actual_demand, demand_level))
        
        # Calculate quantity sold
        quantity = min(actual_demand, tickets_left)
        revenue = price * quantity
        
        return revenue, quantity 