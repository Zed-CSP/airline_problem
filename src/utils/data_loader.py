"""
Data loading and preprocessing utilities.
"""

from pathlib import Path
from typing import Optional, Dict, Any

import pandas as pd
import numpy as np


class FlightDataLoader:
    """Loader for flight pricing data."""
    
    def __init__(self, data_path: str = 'data/synthetic/large_airline_pricing_simulation.csv'):
        """
        Initialize the data loader.
        
        Args:
            data_path: Path to the CSV data file
        """
        self.data_path = Path(data_path)
        self.data: Optional[pd.DataFrame] = None
        self.max_days: int = 0
    
    def load_data(self, class_type: str = 'Business') -> bool:
        """
        Load and preprocess the flight data.
        
        Args:
            class_type: Type of flight class to filter for
            
        Returns:
            bool: True if data was loaded successfully
        """
        try:
            self.data = pd.read_csv(self.data_path)
            print(f"\nLoaded data with columns: {self.data.columns.tolist()}")
            
            # Filter for specified class
            self.data = self.data[self.data['Class'] == class_type]
            print(f"Number of {class_type} class records: {len(self.data)}")
            
            # Get maximum days
            self.max_days = self.data['Days Before Departure'].max()
            print(f"Maximum days before departure: {self.max_days}")
            
            return True
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False
    
    def get_flight_data(self, 
                       flight_id: int, 
                       days_before: int) -> Dict[str, Any]:
        """
        Get data for a specific flight and day.
        
        Args:
            flight_id: Flight identifier
            days_before: Days before departure
            
        Returns:
            Dict containing demand and historical price
        """
        if self.data is None:
            return {'demand': np.random.uniform(20, 40), 'price': None}
        
        try:
            flight_data = self.data.loc[
                (self.data['Flight ID'] == flight_id) & 
                (self.data['Days Before Departure'] == days_before)
            ].iloc[0]
            
            return {
                'demand': float(flight_data['Demand']),
                'price': float(flight_data['Price'])
            }
            
        except Exception as e:
            print(f"Error getting flight data: {str(e)}")
            return {'demand': np.random.uniform(20, 40), 'price': None}
    
    @property
    def available_flight_ids(self) -> list:
        """Get list of available flight IDs in the data."""
        if self.data is None:
            return []
        return sorted(self.data['Flight ID'].unique()) 