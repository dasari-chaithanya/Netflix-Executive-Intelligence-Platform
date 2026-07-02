from app.viewmodels.base import BaseViewModel

class GenreViewModel(BaseViewModel):
    def get_data(self):
        if self.df.empty:
            return {"valid": False}
            
        genres = self.df['listed_in'].dropna().str.split(',').explode().str.strip()
        top_genres = genres.value_counts().head(10).to_dict()
        
        return {
            "valid": True,
            "top_genres": top_genres
        }
