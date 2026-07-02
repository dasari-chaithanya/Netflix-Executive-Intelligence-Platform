MOCK_KPIS = {
    "catalog_freshness": {
        "label": "Catalog Freshness",
        "value": "42.5%",
        "delta": "+2.1%",
        "trend": "up",
        "info": "Titles added in the last 24 months vs Total Catalog"
    },
    "average_content_age": {
        "label": "Avg Content Age",
        "value": "5.2 yrs",
        "delta": "-0.3 yrs",
        "trend": "up", # lower age is better freshness
        "info": "Average time since original release year"
    },
    "genre_diversity": {
        "label": "Genre Diversity Index",
        "value": "14",
        "delta": "0",
        "trend": "flat",
        "info": "Count of genres making up 80% of catalog"
    },
    "survival_rate": {
        "label": "Series Survival Rate",
        "value": "34.1%",
        "delta": "-1.2%",
        "trend": "down",
        "info": "TV Shows with >1 season"
    }
}
