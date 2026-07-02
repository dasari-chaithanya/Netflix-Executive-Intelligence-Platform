from app.viewmodels.base import BaseViewModel

class GrowthViewModel(BaseViewModel):
    def get_data(self):
        if self.df.empty:
            return {"valid": False}
        return {
            "valid": True,
            "additions_by_year": self.df['release_year'].value_counts().sort_index().to_dict()
        }
