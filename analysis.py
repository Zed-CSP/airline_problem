import numpy as np
from simulator import FlightSimulator

class PricingAnalysis:
    def __init__(self, n_simulations=100):
        self.n_simulations = n_simulations
        self.simulator = FlightSimulator()
        self.results = []
        
    def run_analysis(self):
        """Run multiple simulations and collect comprehensive metrics."""
        total_revenues = []
        unsold_seats = []
        avg_prices = []
        load_factors = []
        opportunity_costs = []
        
        for _ in range(self.n_simulations):
            result = self.simulator.run_simulation()
            
            # Basic metrics
            total_revenues.append(result['total_revenue'])
            unsold_seats.append(result['remaining_seats'])
            avg_prices.append(np.mean(result['daily_prices']))
            
            # Calculate load factor (percentage of seats sold)
            load_factor = (self.simulator.total_seats - result['remaining_seats']) / self.simulator.total_seats
            load_factors.append(load_factor)
            
            # Calculate opportunity cost (potential revenue lost from unsold seats)
            avg_demand = np.mean(result['daily_demand'])
            avg_price = np.mean(result['daily_prices'])
            potential_revenue = self.simulator.total_seats * avg_price
            opportunity_cost = potential_revenue - result['total_revenue']
            opportunity_costs.append(opportunity_cost)
            
            self.results.append({
                'revenue': result['total_revenue'],
                'unsold_seats': result['remaining_seats'],
                'avg_price': np.mean(result['daily_prices']),
                'load_factor': load_factor,
                'opportunity_cost': opportunity_cost,
                'daily_stats': {
                    'prices': result['daily_prices'],
                    'demand': result['daily_demand'],
                    'sales': result['daily_sales'],
                    'revenue': result['daily_revenue']
                }
            })
    
    def print_analysis(self):
        """Print comprehensive analysis of the pricing strategy."""
        if not self.results:
            self.run_analysis()
            
        revenues = [r['revenue'] for r in self.results]
        unsold = [r['unsold_seats'] for r in self.results]
        load_factors = [r['load_factor'] for r in self.results]
        opportunity_costs = [r['opportunity_cost'] for r in self.results]
        
        print("\n=== PRICING STRATEGY ANALYSIS ===")
        print(f"\nBased on {self.n_simulations} simulations:")
        
        print("\n1. Revenue Metrics:")
        print(f"   Average Revenue: ${np.mean(revenues):.2f}")
        print(f"   Revenue Std Dev: ${np.std(revenues):.2f}")
        print(f"   Min Revenue: ${np.min(revenues):.2f}")
        print(f"   Max Revenue: ${np.max(revenues):.2f}")
        
        print("\n2. Capacity Utilization:")
        print(f"   Average Unsold Seats: {np.mean(unsold):.1f}")
        print(f"   Average Load Factor: {np.mean(load_factors):.1%}")
        print(f"   Load Factor Std Dev: {np.std(load_factors):.1%}")
        
        print("\n3. Loss Analysis:")
        print(f"   Average Opportunity Cost: ${np.mean(opportunity_costs):.2f}")
        print(f"   Worst Case Loss: ${np.max(opportunity_costs):.2f}")
        
        # Analyze daily patterns
        daily_prices = np.array([r['daily_stats']['prices'] for r in self.results])
        daily_sales = np.array([r['daily_stats']['sales'] for r in self.results])
        
        print("\n4. Daily Patterns:")
        print("   Average Price by Week:")
        weekly_prices = np.mean(daily_prices.reshape(-1, 7), axis=1)
        for week, avg_price in enumerate(weekly_prices, 1):
            print(f"   Week {week}: ${avg_price:.2f}")
            
        print("\n5. Risk Analysis:")
        revenue_at_risk = np.percentile(revenues, 5)
        print(f"   5% Value at Risk: ${np.mean(revenues) - revenue_at_risk:.2f}")
        print(f"   Revenue Volatility: {np.std(revenues) / np.mean(revenues):.1%}")
        
        # Calculate optimal revenue scenarios
        max_revenue_sim = self.results[np.argmax(revenues)]
        print("\n6. Best Performance Analysis:")
        print(f"   Best Revenue: ${max_revenue_sim['revenue']:.2f}")
        print(f"   With Load Factor: {max_revenue_sim['load_factor']:.1%}")
        print(f"   And Average Price: ${max_revenue_sim['avg_price']:.2f}")

def main():
    analyzer = PricingAnalysis(n_simulations=100)
    analyzer.run_analysis()
    analyzer.print_analysis()

if __name__ == "__main__":
    main() 