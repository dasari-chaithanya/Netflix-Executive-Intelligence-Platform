from app.viewmodels.base import BaseViewModel

class GenreViewModel(BaseViewModel):
    def get_data(self):
        if self.df.empty:
            return {"is_empty": True}
            
        genres = self.df['genres'].dropna().astype(str).str.split(',').explode().str.strip()
        genre_counts = genres.value_counts().reset_index()
        genre_counts.columns = ['Genre', 'Volume']
        
        return {
            "is_empty": False,
            "genre_df": genre_counts.head(15)
        }
