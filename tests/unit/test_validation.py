import pytest
import pandas as pd
from src.validation.contracts import DataContract, DataContractError

def test_data_contract_missing_columns():
    schema = {'id': {'nullable': False}, 'name': {'nullable': True}}
    contract = DataContract("Test", schema)
    
    df = pd.DataFrame({'id': [1, 2]})
    with pytest.raises(DataContractError, match="Missing required columns"):
        contract.validate(df)

def test_data_contract_nulls():
    schema = {'id': {'nullable': False}}
    contract = DataContract("Test", schema)
    
    df = pd.DataFrame({'id': [1, None]})
    with pytest.raises(DataContractError, match="contains 1 null values"):
        contract.validate(df)

def test_data_contract_custom_validation():
    schema = {'age': {'validation': lambda s: (s > 0).all()}}
    contract = DataContract("Test", schema)
    
    df = pd.DataFrame({'age': [10, -5]})
    with pytest.raises(DataContractError, match="failed custom validation"):
        contract.validate(df)
