import pandas as pd
from collections import Counter

def get_genre_diversity_index(df: pd.DataFrame) -> int:
    """
    Calculates the Genre Diversity Index.
    Formula: Count of unique genres making up 80% of the catalog.
    """
    if 'genres' not in df.columns:
        raise ValueError("DataFrame must contain 'genres' column.")
        
    all_genres = []
    for g_list in df['genres'].dropna():
        all_genres.extend(g_list)
        
    if not all_genres:
        return 0
        
    genre_counts = Counter(all_genres)
    total_tags = len(all_genres)
    
    # Sort genres by count descending
    sorted_genres = genre_counts.most_common()
    
    cumulative_sum = 0
    target = 0.8 * total_tags
    
    index = 0
    for genre, count in sorted_genres:
        cumulative_sum += count
        index += 1
        if cumulative_sum >= target:
            break
            
    return index
