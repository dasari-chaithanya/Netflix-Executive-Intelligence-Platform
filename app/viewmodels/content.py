from app.viewmodels.base import BaseViewModel
import pandas as pd

class ContentViewModel(BaseViewModel):
    def get_data(self):
        if self.df.empty:
            return {"is_empty": True}
            
        # Distribution (Bar Chart Data)
        dist_df = self.df['type'].value_counts().reset_index()
        dist_df.columns = ['Content Type', 'Count']
        
        # Release Trends (Line Chart Data)
        trend_df = self.df.groupby(['release_year', 'type']).size().reset_index(name='Count')
        
        return {
            "is_empty": False,
            "distribution_df": dist_df,
            "trend_df": trend_df
        }
