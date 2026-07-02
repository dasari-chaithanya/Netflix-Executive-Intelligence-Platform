from app.viewmodels.base import BaseViewModel

class GeographyViewModel(BaseViewModel):
    def get_data(self):
        if self.df.empty:
            return {"valid": False}
            
        countries = self.df['country'].dropna().str.split(',').explode().str.strip()
        top_countries = countries.value_counts().head(10).to_dict()
        
        return {
            "valid": True,
            "top_countries": top_countries
        }
