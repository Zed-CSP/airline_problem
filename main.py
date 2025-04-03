"""
Main script for running airline pricing simulations.
"""

import numpy as np
from src.simulation.simulator import FlightSimulator


def main():
    """Run airline pricing simulations."""
    # Initialize simulator
    simulator = FlightSimulator(
        total_seats=50,
        data_path='assets/SynthData/large_airline_pricing_simulation.csv'
    )
    
    # Run simulations for multiple flights
    n_simulations = 3
    total_revenues = []
    
    # Get available flights
    flight_ids = simulator.available_flights[:n_simulations]
    if not flight_ids:
        flight_ids = range(1, n_simulations + 1)
    
    # Run simulations
    for flight_id in flight_ids:
        results = simulator.run_simulation(flight_id)
        simulator.print_results(results)
        total_revenues.append(results['total_revenue'])
    
    # Print summary statistics
    print(f"\nSummary Statistics (over {n_simulations} flights):")
    print(f"Average Revenue: ${np.mean(total_revenues):.2f}")
    print(f"Standard Deviation: ${np.std(total_revenues):.2f}")
    print(f"Min Revenue: ${np.min(total_revenues):.2f}")
    print(f"Max Revenue: ${np.max(total_revenues):.2f}")


if __name__ == "__main__":
    main() 