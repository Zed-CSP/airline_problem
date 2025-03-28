import numpy as np
from pricing_function import pricing_function, calculate_expected_revenue

class FlightSimulator:
    def __init__(self, total_seats=100, days_until_flight=30):
        self.total_seats = total_seats
        self.days_until_flight = days_until_flight
        self.remaining_seats = total_seats
        self.total_revenue = 0
        self.daily_revenue = []
        self.daily_prices = []
        self.daily_demand = []
        self.daily_sales = []
    
    def simulate_day(self, demand_level):
        """Simulate one day of ticket sales."""
        if self.remaining_seats <= 0 or self.days_until_flight <= 0:
            return 0
        
        # Get price from pricing function
        price = pricing_function(self.days_until_flight, self.remaining_seats, demand_level)
        
        # Calculate quantity sold
        quantity = min(demand_level - price, self.remaining_seats)
        
        # Update state
        revenue = price * quantity
        self.total_revenue += revenue
        self.remaining_seats -= quantity
        self.days_until_flight -= 1
        
        # Record daily statistics
        self.daily_revenue.append(revenue)
        self.daily_prices.append(price)
        self.daily_demand.append(demand_level)
        self.daily_sales.append(quantity)
        
        return revenue
    
    def run_simulation(self):
        """Run a complete simulation with random demand levels."""
        self.remaining_seats = self.total_seats
        self.days_until_flight = 30
        self.total_revenue = 0
        self.daily_revenue = []
        self.daily_prices = []
        self.daily_demand = []
        self.daily_sales = []
        
        for _ in range(self.days_until_flight):
            # Generate random demand level between 100 and 200
            demand_level = np.random.uniform(100, 200)
            self.simulate_day(demand_level)
        
        return {
            'total_revenue': self.total_revenue,
            'remaining_seats': self.remaining_seats,
            'daily_revenue': self.daily_revenue,
            'daily_prices': self.daily_prices,
            'daily_demand': self.daily_demand,
            'daily_sales': self.daily_sales
        }

def main():
    # Run multiple simulations to get average performance
    n_simulations = 100
    total_revenues = []
    
    for i in range(n_simulations):
        simulator = FlightSimulator()
        results = simulator.run_simulation()
        total_revenues.append(results['total_revenue'])
        
        if i == 0:  # Print details of first simulation
            print("\nFirst Simulation Results:")
            print(f"Total Revenue: ${results['total_revenue']:.2f}")
            print(f"Remaining Seats: {results['remaining_seats']}")
            print("\nDaily Statistics:")
            for day in range(len(results['daily_revenue'])):
                print(f"Day {day+1}:")
                print(f"  Price: ${results['daily_prices'][day]:.2f}")
                print(f"  Demand: {results['daily_demand'][day]:.2f}")
                print(f"  Sales: {results['daily_sales'][day]}")
                print(f"  Revenue: ${results['daily_revenue'][day]:.2f}")
    
    # Print summary statistics
    print(f"\nSummary Statistics (over {n_simulations} simulations):")
    print(f"Average Revenue: ${np.mean(total_revenues):.2f}")
    print(f"Standard Deviation: ${np.std(total_revenues):.2f}")
    print(f"Min Revenue: ${np.min(total_revenues):.2f}")
    print(f"Max Revenue: ${np.max(total_revenues):.2f}")

if __name__ == "__main__":
    main() 