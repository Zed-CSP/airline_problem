import numpy as np
import pandas as pd
from pricing_function import pricing_function, calculate_expected_revenue

class FlightSimulator:
    def __init__(self, total_seats=50):  # Reduced seats for business class
        self.total_seats = total_seats
        self.remaining_seats = total_seats
        self.total_revenue = 0
        self.daily_revenue = []
        self.daily_prices = []
        self.daily_demand = []
        self.daily_sales = []
        
        # Load synthetic data
        try:
            self.synth_data = pd.read_csv('assets/SynthData/large_airline_pricing_simulation.csv')
            print("\nLoaded synthetic data with columns:", self.synth_data.columns.tolist())
            print("\nSample of synthetic data:")
            print(self.synth_data.head())
            self.use_synth_data = True
            
            # Get maximum days from data
            self.max_days = self.synth_data['Days Before Departure'].max()
            print(f"\nMaximum days before departure in data: {self.max_days}")
            
            # Filter for business class only
            self.synth_data = self.synth_data[self.synth_data['Class'] == 'Business']
            print(f"Number of business class records: {len(self.synth_data)}")
        except Exception as e:
            print(f"Warning: Could not load synthetic data ({str(e)}). Using random generation instead.")
            self.use_synth_data = False
    
    def get_demand_level(self, day_index, flight_index=0):
        """Get demand level either from synthetic data or generate randomly."""
        if self.use_synth_data:
            try:
                # Convert day_index to match the data format
                days_before_departure = self.max_days - day_index
                
                # Get demand for this flight and day
                demand = self.synth_data.loc[
                    (self.synth_data['Flight ID'] == flight_index) & 
                    (self.synth_data['Days Before Departure'] == days_before_departure),
                    'Demand'
                ].iloc[0]
                
                return float(demand)
            except Exception as e:
                print(f"Warning: Error reading synthetic data ({str(e)}). Falling back to random generation.")
                return np.random.uniform(20, 40)  # Adjusted for business class
        else:
            return np.random.uniform(20, 40)  # Adjusted for business class
    
    def get_historical_price(self, day_index, flight_index=0):
        """Get historical price from synthetic data if available."""
        if self.use_synth_data:
            try:
                days_before_departure = self.max_days - day_index
                price = self.synth_data.loc[
                    (self.synth_data['Flight ID'] == flight_index) & 
                    (self.synth_data['Days Before Departure'] == days_before_departure),
                    'Price'
                ].iloc[0]
                return float(price)
            except Exception:
                return None
        return None
    
    def simulate_day(self, day_index, flight_index=0):
        """Simulate one day of ticket sales."""
        if self.remaining_seats <= 0:
            return 0
        
        # Get demand level from synthetic data
        demand_level = self.get_demand_level(day_index, flight_index)
        
        # Get price from pricing function
        price = pricing_function(self.max_days - day_index, self.remaining_seats, demand_level)
        
        # Get historical price for comparison
        historical_price = self.get_historical_price(day_index, flight_index)
        if historical_price is not None:
            print(f"Day {day_index + 1}: Our price: ${price:.2f}, Historical price: ${historical_price:.2f}, Demand: {demand_level:.1f}")
        
        # Calculate quantity sold using the revenue calculator
        revenue = calculate_expected_revenue(price, demand_level, self.remaining_seats)
        quantity = revenue / price if price > 0 else 0
        
        # Update state
        self.total_revenue += revenue
        self.remaining_seats -= quantity
        
        # Record daily statistics
        self.daily_revenue.append(revenue)
        self.daily_prices.append(price)
        self.daily_demand.append(demand_level)
        self.daily_sales.append(quantity)
        
        return revenue
    
    def run_simulation(self, flight_index=0):
        """Run a complete simulation for one flight."""
        self.remaining_seats = self.total_seats
        self.total_revenue = 0
        self.daily_revenue = []
        self.daily_prices = []
        self.daily_demand = []
        self.daily_sales = []
        
        print(f"\nRunning simulation for Flight ID: {flight_index}")
        for day in range(self.max_days):
            self.simulate_day(day, flight_index)
        
        return {
            'total_revenue': self.total_revenue,
            'remaining_seats': self.remaining_seats,
            'daily_revenue': self.daily_revenue,
            'daily_prices': self.daily_prices,
            'daily_demand': self.daily_demand,
            'daily_sales': self.daily_sales
        }

def main():
    # Run simulations for a few different flights
    n_simulations = 3  # Reduced number of simulations to better see the comparison
    total_revenues = []
    
    simulator = FlightSimulator()
    
    for i in range(n_simulations):
        results = simulator.run_simulation(flight_index=i+1)  # Using Flight ID starting from 1
        total_revenues.append(results['total_revenue'])
        
        print(f"\nFlight {i+1} Results:")
        print(f"Total Revenue: ${results['total_revenue']:.2f}")
        print(f"Remaining Seats: {results['remaining_seats']:.1f}")
        print(f"Average Price: ${np.mean(results['daily_prices']):.2f}")
        print(f"Average Demand: {np.mean(results['daily_demand']):.1f}")
        print(f"Total Sales: {sum(results['daily_sales']):.1f}")
    
    # Print summary statistics
    print(f"\nSummary Statistics (over {n_simulations} flights):")
    print(f"Average Revenue: ${np.mean(total_revenues):.2f}")
    print(f"Standard Deviation: ${np.std(total_revenues):.2f}")
    print(f"Min Revenue: ${np.min(total_revenues):.2f}")
    print(f"Max Revenue: ${np.max(total_revenues):.2f}")

if __name__ == "__main__":
    main() 