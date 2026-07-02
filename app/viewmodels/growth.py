from app.viewmodels.base import BaseViewModel
import pandas as pd

class GrowthViewModel(BaseViewModel):
    def get_data(self):
        if self.df.empty or 'date_added' not in self.df.columns:
            return {"is_empty": True}
            
        # Process date added for growth
        df_copy = self.df.copy()
        df_copy['date_added'] = pd.to_datetime(df_copy['date_added'], errors='coerce')
        df_copy = df_copy.dropna(subset=['date_added'])
        
        df_copy['year_added'] = df_copy['date_added'].dt.year
        growth_df = df_copy.groupby(['year_added', 'type']).size().reset_index(name='Additions')
        
        return {
            "is_empty": False,
            "growth_df": growth_df
        }
