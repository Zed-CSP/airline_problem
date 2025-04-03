"""
Flight pricing simulator implementation.
"""

from typing import Dict, Any, List
import numpy as np

from ..models.pricing_model import BusinessClassPricingModel
from ..utils.data_loader import FlightDataLoader


class FlightSimulator:
    """Simulator for testing airline pricing strategies."""
    
    def __init__(self, 
                 total_seats: int = 50,
                 data_path: str = 'data/synthetic/large_airline_pricing_simulation.csv'):
        """
        Initialize the simulator.
        
        Args:
            total_seats: Number of seats available
            data_path: Path to the synthetic data file
        """
        self.total_seats = total_seats
        self.remaining_seats = total_seats
        self.total_revenue = 0.0
        
        # Initialize components
        self.data_loader = FlightDataLoader(data_path)
        self.pricing_model = BusinessClassPricingModel()
        
        # Statistics tracking
        self.daily_stats: Dict[str, List[float]] = {
            'revenue': [],
            'prices': [],
            'demand': [],
            'sales': []
        }
        
        # Load data
        self.use_synthetic = self.data_loader.load_data()
    
    def simulate_day(self, day_index: int, flight_id: int) -> float:
        """
        Simulate one day of ticket sales.
        
        Args:
            day_index: Current day index
            flight_id: Flight identifier
            
        Returns:
            float: Revenue generated this day
        """
        if self.remaining_seats <= 0:
            return 0.0
        
        # Get flight data
        flight_data = self.data_loader.get_flight_data(
            flight_id=flight_id,
            days_before=self.data_loader.max_days - day_index
        )
        
        # Calculate optimal price
        price = self.pricing_model.calculate_price(
            days_left=self.data_loader.max_days - day_index,
            tickets_left=self.remaining_seats,
            demand_level=flight_data['demand']
        )
        
        # Calculate revenue and sales
        revenue, quantity = self.pricing_model.calculate_revenue(
            price=price,
            demand_level=flight_data['demand'],
            tickets_left=self.remaining_seats
        )
        
        # Update state
        self.total_revenue += revenue
        self.remaining_seats -= quantity
        
        # Record statistics
        self.daily_stats['revenue'].append(revenue)
        self.daily_stats['prices'].append(price)
        self.daily_stats['demand'].append(flight_data['demand'])
        self.daily_stats['sales'].append(quantity)
        
        # Print comparison with historical price if available
        if flight_data['price'] is not None:
            print(f"Day {day_index + 1}: "
                  f"Our price: ${price:.2f}, "
                  f"Historical: ${flight_data['price']:.2f}, "
                  f"Demand: {flight_data['demand']:.1f}")
        
        return revenue
    
    def run_simulation(self, flight_id: int) -> Dict[str, Any]:
        """
        Run a complete simulation for one flight.
        
        Args:
            flight_id: Flight identifier
            
        Returns:
            Dict containing simulation results
        """
        # Reset state
        self.remaining_seats = self.total_seats
        self.total_revenue = 0.0
        self.daily_stats = {key: [] for key in self.daily_stats}
        
        print(f"\nRunning simulation for Flight ID: {flight_id}")
        
        # Run simulation for each day
        for day in range(self.data_loader.max_days):
            self.simulate_day(day, flight_id)
        
        return {
            'total_revenue': self.total_revenue,
            'remaining_seats': self.remaining_seats,
            'daily_revenue': self.daily_stats['revenue'],
            'daily_prices': self.daily_stats['prices'],
            'daily_demand': self.daily_stats['demand'],
            'daily_sales': self.daily_stats['sales']
        }
    
    def print_results(self, results: Dict[str, Any]) -> None:
        """
        Print detailed results from a simulation.
        
        Args:
            results: Simulation results dictionary
        """
        print("\nSimulation Results:")
        print(f"Total Revenue: ${results['total_revenue']:.2f}")
        print(f"Remaining Seats: {results['remaining_seats']:.1f}")
        print(f"Average Price: ${np.mean(results['daily_prices']):.2f}")
        print(f"Average Demand: {np.mean(results['daily_demand']):.1f}")
        print(f"Total Sales: {sum(results['daily_sales']):.1f}")
        
    @property
    def available_flights(self) -> List[int]:
        """Get list of available flight IDs."""
        return self.data_loader.available_flight_ids 