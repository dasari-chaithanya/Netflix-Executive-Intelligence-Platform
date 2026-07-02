import pandas as pd
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class DataContractError(Exception):
    """Raised when a dataframe violates its schema contract."""
    pass

class DataContract:
    def __init__(self, stage: str, schema: Dict[str, Any]):
        self.stage = stage
        self.schema = schema
        
    def validate(self, df: pd.DataFrame) -> bool:
        """Validates the DataFrame against the defined schema."""
        errors = []
        
        # Check required columns
        missing_cols = set(self.schema.keys()) - set(df.columns)
        if missing_cols:
            errors.append(f"Missing required columns: {missing_cols}")
            
        for col, rules in self.schema.items():
            if col not in df.columns:
                continue
                
            # Check datatype if specified
            if 'dtype' in rules:
                expected_type = rules['dtype']
                # Allow pandas generic object dtype for lists/strings in bronze/silver
                if expected_type != 'object' and expected_type != 'list':
                    try:
                        if not pd.api.types.is_dtype_equal(df[col].dtype, expected_type):
                            # Attempt loose check for datetime/numeric
                            if expected_type == 'datetime64[ns]' and not pd.api.types.is_datetime64_any_dtype(df[col]):
                                errors.append(f"Column {col} has dtype {df[col].dtype}, expected {expected_type}")
                            elif expected_type == 'int64' and not pd.api.types.is_numeric_dtype(df[col]):
                                errors.append(f"Column {col} has dtype {df[col].dtype}, expected {expected_type}")
                    except Exception:
                        pass
                        
            # Check nulls
            if not rules.get('nullable', True):
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    errors.append(f"Column {col} contains {null_count} null values (nullable=False)")
                    
            # Check custom validation
            if 'validation' in rules:
                val_func = rules['validation']
                try:
                    if not val_func(df[col]):
                        errors.append(f"Column {col} failed custom validation")
                except Exception as e:
                    errors.append(f"Column {col} validation raised exception: {e}")
                    
        if errors:
            error_msg = f"Data Contract Violation in {self.stage} stage:\n" + "\n".join(errors)
            logger.error(error_msg)
            raise DataContractError(error_msg)
            
        logger.info(f"Data Contract validated successfully for {self.stage} stage.")
        return True

# Define Schemas

RAW_SCHEMA = {
    'show_id': {'nullable': False},
    'type': {'nullable': False},
    'title': {'nullable': False},
    'director': {'nullable': True},
    'cast': {'nullable': True},
    'country': {'nullable': True},
    'date_added': {'nullable': True},
    'release_year': {'nullable': False, 'validation': lambda s: (s >= 1920).all()},
    'rating': {'nullable': True},
    'duration': {'nullable': True},
    'listed_in': {'nullable': False},
    'description': {'nullable': True}
}

GOLD_SCHEMA = {
    'show_id': {'nullable': False},
    'type': {'nullable': False, 'validation': lambda s: s.isin(['Movie', 'TV Show']).all()},
    'title': {'nullable': False},
    'director': {'nullable': True, 'dtype': 'object'},
    'cast': {'nullable': True, 'dtype': 'object'},
    'countries': {'nullable': False, 'dtype': 'object'}, # List of strings
    'date_added': {'nullable': True, 'dtype': 'datetime64[ns]'},
    'release_year': {'nullable': False, 'dtype': 'int64', 'validation': lambda s: (s >= 1920).all()},
    'rating': {'nullable': False},
    'duration_mins': {'nullable': True, 'dtype': 'float64'},
    'duration_seasons': {'nullable': True, 'dtype': 'float64'},
    'genres': {'nullable': False, 'dtype': 'object'},
    'release_decade': {'nullable': False, 'dtype': 'int64'}
}

raw_contract = DataContract(stage="Raw", schema=RAW_SCHEMA)
gold_contract = DataContract(stage="Gold", schema=GOLD_SCHEMA)
