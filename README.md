# Airline Ticket Pricing Optimization

This project implements a dynamic pricing system for airline tickets, with a focus on business class pricing optimization.

## Project Structure

```
airline_pricing/
├── src/
│   ├── models/
│   │   └── pricing_model.py    # Pricing algorithm implementation
│   ├── simulation/
│   │   └── simulator.py        # Simulation environment
│   └── utils/
│       └── data_loader.py      # Data loading utilities
├── data/
│   └── synthetic/             # Synthetic data directory
├── tests/                     # Test directory
├── main.py                    # Main script
└── requirements.txt           # Dependencies
```

## Features

- Dynamic pricing based on:
  - Current demand level
  - Remaining inventory
  - Time until departure
  - Historical data
- Business class specific optimizations
- Comparison with historical pricing
- Detailed performance analytics

## Installation

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the simulation:
```bash
python main.py
```

The simulator will:
1. Load synthetic data
2. Run pricing simulations for multiple flights
3. Compare results with historical data
4. Display detailed statistics

## Pricing Model

The pricing model considers multiple factors:
- Base price for business class
- Demand elasticity
- Inventory pressure
- Time pressure
- Special case adjustments (high demand, last-minute, etc.)

## Data

The system uses synthetic data from `assets/SynthData/large_airline_pricing_simulation.csv` with the following structure:
- Flight ID: Unique flight identifier
- Days Before Departure: Number of days until the flight
- Class: Ticket class (Business/Economy)
- Price: Historical price
- Demand: Demand level for that day

## Performance Metrics

The system tracks:
- Total revenue
- Average price
- Load factor
- Demand patterns
- Historical price comparison
