from app.viewmodels.base import BaseViewModel

class ContentViewModel(BaseViewModel):
    def get_data(self):
        if self.df.empty:
            return {"valid": False}
        return {
            "valid": True,
            "rating_distribution": self.df['rating'].value_counts().to_dict()
        }
