# Airline Ticket Pricing Problem

This project implements a solution for Aviato.com's airline ticket pricing problem. The goal is to maximize revenue by dynamically pricing airline tickets based on various factors.

## Problem Description

For each flight, a pricing function is run once per simulated day to set that day's ticket price. The function must consider:
- Number of days until the flight
- Number of seats remaining
- Current demand level (known for current day, uniform distribution 100-200 for future days)

The quantity of tickets sold follows the formula:
```
quantity_sold = min(demand_level - price, remaining_seats)
```

## Solution Components

1. `pricing_function.py`: Contains the main pricing algorithm
2. `simulator.py`: Simulates the ticket sales environment
3. `analysis.py`: Tools for analyzing the performance of different pricing strategies

## Usage

Run the simulator to test the pricing strategy:
```bash
python simulator.py
```

## Implementation Details

The pricing function uses a dynamic programming approach to optimize revenue by:
1. Considering the current demand level
2. Estimating future demand based on the uniform distribution
3. Balancing immediate revenue with future opportunities
4. Adjusting prices based on remaining inventory and time until departure
