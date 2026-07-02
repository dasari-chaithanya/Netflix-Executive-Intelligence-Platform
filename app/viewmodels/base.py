import pandas as pd
from typing import Dict, Any
from app.data.loader import load_processed_data
from app.data.filters import apply_global_filters
from app.state.store import get_filters

class BaseViewModel:
    """
    Base class for all ViewModels.
    Handles loading the data and applying the global session filters.
    """
    def __init__(self):
        self.raw_df = load_processed_data()
        self.filters = get_filters()
        self.df = apply_global_filters(self.raw_df, self.filters)
        
    def get_data(self) -> Dict[str, Any]:
        """Override in subclasses to return the specific data contract for the page."""
        raise NotImplementedError
