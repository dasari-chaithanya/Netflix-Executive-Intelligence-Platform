from app.viewmodels.base import BaseViewModel

class GeographyViewModel(BaseViewModel):
    def get_data(self):
        if self.df.empty:
            return {"is_empty": True}
            
        # Explode countries since they are comma separated
        # For safety, ensure it is a string first
        countries = self.df['country'].dropna().astype(str).str.split(',').explode().str.strip()
        country_counts = countries.value_counts().reset_index()
        country_counts.columns = ['Country', 'Volume']
        
        # ISO-3 mapping would ideally happen in the Analytics Engine. We will mock the ISO codes for the map placeholder.
        # This is safe as it's just visual plumbing for M3.
        
        return {
            "is_empty": False,
            "country_df": country_counts.head(15), # Top 15 for Bar
            "map_df": country_counts # All for map
        }
